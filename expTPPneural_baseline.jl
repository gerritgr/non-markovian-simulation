import Pkg
using DataStructures
using StatsBase
using DataFrames
using CSV
using Plots


#
# call with:   julia expTPPneural_baseline.jl 10 graph.txt  out_TPPneural_baseline.txt
# (for evaluation use )

#*********************************
#  Type Alias
#*********************************
struct Infected end
struct Susceptible end
State = Union{Infected,Susceptible}

const Real = Float64
const Node = Int64
const Graph = Dict{Node,Array{Node,1}}
const NodeTimes = Dict{Node,Real}
const Labeling = Array{State,1}
const StorageType = Dict{String,Array{Any,1}}
const Neighborhood = Array{Node,1}
const NeighborhoodTimes = Dict{Node,Real}
const NeighborhoodStates = Dict{Node,State}


#*********************************
#  Config
#*********************************

const NUMBER_OF_SAVES = 301
const STEP = 1.0/1000.0

function get_actual_inf_rate(src_node::Node, time_from_now::Real, neighbor_restimes::NeighborhoodTimes, neighbor_states::NeighborhoodStates)::Real

    c::Real = 1.0
    b::Real = 1.0
    mu::Real = 0.01
    step_to_inhibit::Int64 = 5

    rate::Real = mu

    for (n,t) in neighbor_restimes
            if (n+src_node) % step_to_inhibit == 0
                c = -1*c
            end
            t_plus = t+time_from_now
            rate += c*(1.0/(t_plus+b))
    end

    rate = max(0, tanh(rate))
    return rate
end

function next_event_time(src_node::Node, residence_time::Real, target_state::State, neighbor_restimes::NeighborhoodTimes, neighbor_states::NeighborhoodStates, horizon::Real)::Tuple{Real,Real}
    local t_e_shift::Real, actual_rate::Real, t_e::Real, tt::Real, number_inf_neighbors::Int64

    c::Real = 1.0
    b::Real = 1.0
    mu::Real = 0.01

    over_approx_rate::Real = 1.0

    t_e = 0.0
    while true
        if t_e  > horizon
            return 100000.0+rand(), 100000.0 #Dummy
        end
        t_e_shift = -log(rand())/over_approx_rate
        t_e += t_e_shift
        actual_rate = get_actual_inf_rate(src_node, t_e, neighbor_restimes,neighbor_states)
        if rand()<actual_rate/over_approx_rate
            return t_e, actual_rate
        end
    end

    return rand()+100000.0, 10000.0 #dummy careful!
end

#function infection(residence_time::Real, neighbor_restimes::NeighborhoodTimes, neighbor_states::NeighborhoodStates)::Real
#    rate_sum::Real = 0.0
#    mu::Real = 0.4
#    for (n, s) in neighbor_states
#        if s==Infected()
#            rate_sum += mu*exp(-mu * neighbor_restimes[n])
#        end
#    end
#    return rate_sum
#end#
#
#function recovery(residence_time::Real, neighbor_restimes::NeighborhoodTimes, neighbor_states::NeighborhoodStates)::Real
#    mu::Real = 1.0
#    return mu*exp(-mu * residence_time)
#end



#*********************************
#  Data Structures
#*********************************

mutable struct Model
    horizon::Real
    graph::Graph
    time_last_switch::NodeTimes  # map from node to time when node last changed
    outfile::String
    labeling::Labeling
    current_time::Real
    storage::StorageType
    remaining_savepoints::Array{Real}
    current_counts::Dict{Union{Infected, Susceptible},Int64}
    time_info::Dict{String,Union{Real,Int64}}
end

mutable struct Reaction
    src_state::State
    target_state::State
    original_rate::Real
end


const ReactionMap = Dict{Node, Reaction}
const EventQueue = PriorityQueue{Node,Real,Base.Order.ForwardOrdering}
const EPSILON = 0.00000000001


#*********************************
#  Output
#*********************************

function write_model(model)
    df = DataFrame(model.storage)
    CSV.write(model.outfile, df)

    gr()
    plot(model.storage["Time"], model.storage["Infected"], label="Infected")
    plot!(model.storage["Time"], model.storage["Susceptible"], label="Susceptible")
    #scatter!(numpirates, globaltemperatures, label="points")
    xlabel!("Time")
    ylabel!("#Nodes in State")
    plot_path = replace(model.outfile, ".txt" => "") * ".pdf"
    plot_path = replace(plot_path, ".csv" => "") #TODO better
    savefig(plot_path)
    #savefig(model.outfile+".pdf")

    #write time
    time_path = replace(model.outfile, ".txt" => "") * "__time__.txt"
    time_path = replace(time_path, ".csv" => "") #TODO better

    model.time_info["time_per_real_step"] = model.time_info["elapsed_time"]/(model.time_info["all_steps"])
    df_time = DataFrame(model.time_info)
    CSV.write(time_path, df_time)
end

function save!(model::Model)
    while length(model.remaining_savepoints) > 0 && model.current_time > model.remaining_savepoints[end] # length check important becaue of this loop
        push!(model.storage["Infected"], model.current_counts[Infected()])
        push!(model.storage["Susceptible"], model.current_counts[Susceptible()])
        push!(model.storage["Time"], model.remaining_savepoints[end])
        pop!(model.remaining_savepoints)
        println("current counts: \t",model.current_counts)
    end
end


#*********************************
#  Simulation
#*********************************

function step!(model::Model, pq::EventQueue, rm::ReactionMap)

    if length(pq) == 0
        model.current_time = model.horizon+EPSILON
        save!(model)
        return
    end

    node::Node, event_time::Real = dequeue_pair!(pq)
    model.time_last_switch[node] = event_time
    model.time_info["all_steps"] += 1
    node_reaction::Reaction = rm[node]
    model.current_time = event_time
    save!(model)

    #apply
    set_state!(node, model, node_reaction.target_state)

    if node_reaction.target_state == Infected()
        model.current_counts[Infected()] += 1
        model.current_counts[Susceptible()] -= 1
    else
        model.current_counts[Infected()] -= 1
        model.current_counts[Susceptible()] += 1
    end

    #create new event for src node
    reaction_new::Reaction, event_time_new::Real = create_event(node, model)
    pq[node] = event_time_new
    rm[node] = reaction_new


    #create new event for neighbors
    neighbors::Array{Node} = model.graph[node]
    for neighbor in neighbors
        reaction_neighbor::Reaction, event_time_neighbor::Real = create_event(neighbor, model)
        pq[neighbor] = event_time_neighbor
        rm[neighbor] = reaction_neighbor
    end

end

function simulation!(model::Model, pq::EventQueue, rm::ReactionMap)
    while model.current_time < model.horizon
        step!(model, pq, rm)
    end
end

#*********************************
#  Init
#*********************************

function get_state(node::Node, model::Model)::State
    return model.labeling[node+1]
end

function set_state!(node::Node, model::Model, new_state::State)
    model.labeling[node+1] = new_state
end

function init_storage(labeling)
    storage::StorageType = Dict("Infected" => [], "Susceptible" => [], "Time" => [])
end


function create_event(src_node::Node, model::Model)::Tuple{Reaction, Real}
    local current_rate::Real, reaction_prob::Real, reaction_time::Real, shifted_neighborhood::NeighborhoodTimes

    src_state::State = get_state(src_node, model)
    src_last_switch::Real = model.time_last_switch[src_node]
    src_restime::Real = model.current_time-src_last_switch
    target_state::State = src_state == Infected() ? Susceptible() : Infected()


    neighbor_nodes::Neighborhood = model.graph[src_node]
    neighbor_states::NeighborhoodStates = Dict(n=>get_state(n, model) for n in neighbor_nodes)
    neighbor_restimes::NeighborhoodTimes = Dict(n=>model.current_time-model.time_last_switch[n] for n in neighbor_nodes)


    t_e::Real, rate::Real = next_event_time(src_node, src_restime, target_state, neighbor_restimes, neighbor_states, model.horizon)
    reaction_time = model.current_time+t_e
    reaction=Reaction(src_state,target_state,rate)
    return reaction, reaction_time
end

    #integral_size::Real = -log(rand()) # exp dist rand variate
    #time_shift::Real = 0.0
    #while model.current_time + time_shift <= model.horizon
    #    time_shift += STEP
    #    shifted_neighbor_restimes = Dict(n=>res_time+time_shift for (n,res_time) in neighbor_restimes) #res_time here is actual res time in future
    #    if target_state == Infected()
    #        current_rate = infection(src_restime+time_shift, shifted_neighbor_restimes, neighbor_states)
    #    else
    #        current_rate = recovery(src_restime+time_shift, shifted_neighbor_restimes, neighbor_states)
    #    end
    #    integral_size -= current_rate*STEP
    #    if integral_size <= 0.5*STEP
    #        reaction_time = model.current_time+time_shift
    #        reaction=Reaction(src_state,target_state,current_rate)
    #        return reaction, reaction_time
    #    end
    #end
    #return Reaction(src_state,target_state,1.0/EPSILON), model.horizon * 10 #dummy
#end


function read_gaph(graph_file)
    graph::Graph = Dict()
    labeling_unsorted = []

    open(graph_file) do f
        for (i, line) in enumerate(eachline(f))
            src_node, label, neighbors = split(line, ";")
            src_node = parse(Node, src_node)
            state::State = label=="S" ? Susceptible() : Infected()
            neighbors = split(neighbors, ",")
            neighbors = [parse(Node, n) for n in neighbors]
            graph[src_node] = neighbors
            push!(labeling_unsorted, (state, src_node))
        end
    end

    sort!(labeling_unsorted, by = x -> x[2])   # Sorting should be unnecessary, code does not work if not sorted anyway
    labeling::Labeling = map(x -> x[1], labeling_unsorted)

    return graph, labeling
end

function init_pq_rm(model::Model)::Tuple{EventQueue, ReactionMap}
    local src_node::Node, neighbors::Array{Node}

    pq::EventQueue = PriorityQueue{Node,Real}()
    rm::ReactionMap = Dict{Node,Reaction}()

    for (src_node, neighbors) in model.graph
        reaction::Reaction, event_time::Real = create_event(src_node, model)
        pq[src_node] = event_time
        rm[src_node] = reaction
    end

    return pq, rm
end


function main()
    local model::Model, pq::EventQueue, rm::ReactionMap

    horizon::Float64 = parse(Float64,ARGS[1])
    graph_file::String = string(ARGS[2])
    graph, labeling = read_gaph(graph_file)
    time_last_switch::NodeTimes = Dict(n=>0.0 for n in keys(graph))
    outfile::String = string(ARGS[3])
    remaining_savepoints = LinRange(horizon, 0, NUMBER_OF_SAVES)
    storage::StorageType = init_storage(labeling)
    current_counts = countmap(labeling)
    time_info = Dict("all_steps"=>0, "elapsed_time"=>-1.0)
    model = Model(horizon, graph, time_last_switch, outfile, labeling, 0.0, storage, remaining_savepoints, current_counts,time_info)

    pq, rm = init_pq_rm(model)

    elapsed_time=@elapsed simulation!(model, pq, rm)

    model.time_info["elapsed_time"]=elapsed_time
    println("time info and count", model.time_info)
    println("el time (in sec): \t", elapsed_time)
    write_model(model)
    return model
end

main()



