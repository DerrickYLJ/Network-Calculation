from pycpa import *
# generate an new system
s = model.System('compare')

# set up all the resouces, or vertexes
v1 = s.bind_resource(model.Resource("CPU1", schedulers.SPNPScheduler()))
v2 = s.bind_resource(model.Resource("BUS1",  schedulers.SPNPScheduler()))
v3 = s.bind_resource(model.Resource("BUS2",  schedulers.SPNPScheduler()))    
v4 = s.bind_resource(model.Resource("BUS3",  schedulers.SPNPScheduler()))    
v5 = s.bind_resource(model.Resource("BUS4",  schedulers.SPNPScheduler()))    
v6 = s.bind_resource(model.Resource("BUS5",  schedulers.SPNPScheduler()))        
v7 = s.bind_resource(model.Resource("CPU2", schedulers.SPNPScheduler()))

# create tasks v1 to v7 with specific values and bind them to those newly-established sources
t1 = v1.bind_task(model.Task("T1", wcet=8, bcet=5, scheduling_parameter=2))
t2 = v2.bind_task(model.Task("T2", wcet=16, bcet=1, scheduling_parameter=2))
t3 = v3.bind_task(model.Task("T3", wcet=510, bcet=1, scheduling_parameter=2))
t4 = v4.bind_task(model.Task("T4", wcet=60, bcet=1, scheduling_parameter=2))
t5 = v5.bind_task(model.Task("T5", wcet=1800, bcet=1, scheduling_parameter=2))
t6 = v6.bind_task(model.Task("T6", wcet=11350, bcet=1, scheduling_parameter=2))
t7 = v7.bind_task(model.Task("T7", wcet=1, bcet=1, scheduling_parameter=2))

# specify precedence constraints and link all the tasks altogether:
t1.link_dependent_task(t2).link_dependent_task(t3).link_dependent_task(t4).link_dependent_task(t5).link_dependent_task(t6).link_dependent_task(t7)

t1.in_event_model = model.PJdEventModel(P=30000, J=0)

# graph the system to visualize the architecture
g = graph.graph_system(s, filename='%s.pdf' % s.name, dotout='%s.dot' % s.name, show=False)

print("\nPerforming analysis of system '%s'" % s.name)
task_results = analysis.analyze_system(s)

# print the worst case response times (WCRTs)
print("Result:")
for r in sorted(s.resources, key=str):
    for t in sorted(r.tasks & set(task_results.keys()), key=str):
        print("%s: wcrt=%d" % (t.name, task_results[t].wcrt))
        print("    b_wcrt=%s" % (task_results[t].b_wcrt_str()))

# specify paths
p1 = s.bind_path(model.Path("P1", [t1, t2, t3, t4, t5, t6, t7]))

paths = [p1]
# perform path analysis
for p in paths:
    best_case_latency, worst_case_latency = path_analysis.end_to_end_latency(p, task_results, n=1)
    print("path %s e2e latency. best case: %d, worst case: %d" % (p.name, best_case_latency, worst_case_latency))