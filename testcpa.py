from pycpa import *
# generate an new system
s = model.System('step1')

# add three resources (2 CPUs, 1 Bus) to the system
# and register the SPP scheduler (and SPNP for the bus)
r1 = s.bind_resource(model.Resource("CPU1", schedulers.SPPScheduler()))
r2 = s.bind_resource(model.Resource("BUS",  schedulers.SPNPScheduler()))    
r3 = s.bind_resource(model.Resource("CPU2", schedulers.SPPScheduler()))

# create and bind tasks to r1
t11 = r1.bind_task(model.Task("T11", wcet=10, bcet=5, scheduling_parameter=2))
t12 = r1.bind_task(model.Task("T12", wcet=3, bcet=1, scheduling_parameter=3))

# create and bind tasks to r2
t21 = r2.bind_task(model.Task("T21", wcet=3, bcet=2, scheduling_parameter=2))
t22 = r2.bind_task(model.Task("T22", wcet=9, bcet=5, scheduling_parameter=3))

# create and bind tasks to r3
t31 = r3.bind_task(model.Task("T31", wcet=5, bcet=3, scheduling_parameter=3))
t32 = r3.bind_task(model.Task("T32", wcet=3, bcet=2, scheduling_parameter=2))

# specify precedence constraints: T11 -> T21 -> T31; T12-> T22 -> T32
t11.link_dependent_task(t21).link_dependent_task(t31)
t12.link_dependent_task(t22).link_dependent_task(t32)

# register a periodic with jitter event model for T11 and T12
t11.in_event_model = model.PJdEventModel(P=30, J=15)
t12.in_event_model = model.PJdEventModel(P=15, J=5)

# graph the system to visualize the architecture
g = graph.graph_system(s, filename='%s.pdf' % s.name, dotout='%s.dot' % s.name, show=False)

# perform the analysis
print("\nPerforming analysis of system '%s'" % s.name)
task_results = analysis.analyze_system(s)

# print the worst case response times (WCRTs)
print("Result:")
for r in sorted(s.resources, key=str):
    for t in sorted(r.tasks & set(task_results.keys()), key=str):
        print("%s: wcrt=%d" % (t.name, task_results[t].wcrt))
        print("    b_wcrt=%s" % (task_results[t].b_wcrt_str()))

# specify paths
p1 = s.bind_path(model.Path("P1", [t11, t21, t31]))
p2 = s.bind_path(model.Path("P2", [t12, t22, t32]))
paths = [p1, p2]
# perform path analysis of selected paths
for p in paths:
    best_case_latency, worst_case_latency = path_analysis.end_to_end_latency(p, task_results, n=1)
    print("path %s e2e latency. best case: %d, worst case: %d" % (p.name, best_case_latency, worst_case_latency))

plot_in = [t11, t12]
# plot input event models of selected tasks
for t in plot_in:
    plot.plot_event_model(t.in_event_model, 7, separate_plots=False, file_format='pdf', file_prefix='event-model-%s'
            % t.name, ticks_at_steps=False)