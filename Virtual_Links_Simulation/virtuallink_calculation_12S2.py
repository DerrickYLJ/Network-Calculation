from pycpa import *

# case 2 : VL2
# ( VL12 -> VL5 -> VL10 ) -> VL2 -> VL7 -> VL9 -> VL6 -> switch A (VL12)to ES1
# generate an new system
s = model.System('compare')

# set up all the resouces, or vertexes
VL12 = s.bind_resource(model.Resource("FromSource", schedulers.SPNPScheduler()))
VL5 = s.bind_resource(model.Resource("VL1", schedulers.SPNPScheduler()))
VL10 = s.bind_resource(model.Resource("VL4", schedulers.SPNPScheduler()))
VL2 = s.bind_resource(model.Resource("VL12", schedulers.SPNPScheduler()))
VL7 = s.bind_resource(model.Resource("VL12", schedulers.SPNPScheduler()))
VL9 = s.bind_resource(model.Resource("VL12", schedulers.SPNPScheduler()))
VL6 = s.bind_resource(model.Resource("VL12", schedulers.SPNPScheduler()))
switchA_to_ES1 = s.bind_resource(model.Resource("switchA_to_ES1", schedulers.SPNPScheduler()))

#create tasks related to the resources
t1 = VL12.bind_task(model.Task("T1", wcet=121, bcet=1, scheduling_parameter=2))
t2 = VL5.bind_task(model.Task("T2", wcet=8, bcet=1, scheduling_parameter=2))
t3 = VL10.bind_task(model.Task("T3", wcet=30, bcet=1, scheduling_parameter=2))
t5 = VL2.bind_task(model.Task("T3", wcet=8, bcet=1, scheduling_parameter=2))
t6 = VL7.bind_task(model.Task("T3", wcet=14, bcet=1, scheduling_parameter=2))
t7 = VL9.bind_task(model.Task("T4", wcet=121, bcet=1, scheduling_parameter=2))
t8 = VL6.bind_task(model.Task("T4", wcet=8, bcet=1, scheduling_parameter=2))
t9 = switchA_to_ES1.bind_task(model.Task("T4", wcet=121, bcet=1, scheduling_parameter=2))


# specify precedence constraints and link all the tasks altogether:
t1.link_dependent_task(t2).link_dependent_task(t3).link_dependent_task(t5).link_dependent_task(t6).link_dependent_task(t7).link_dependent_task(t8).link_dependent_task(t9)

t1.in_event_model = model.PJdEventModel(P=16000, J=0)

print("\nPerforming analysis of system '%s'" % s.name)
task_results = analysis.analyze_system(s)

# print the worst case response times (WCRTs)
print("Result:")
for r in sorted(s.resources, key=str):
    for t in sorted(r.tasks & set(task_results.keys()), key=str):
        print("%s: wcrt=%d" % (t.name, task_results[t].wcrt))
        print("    b_wcrt=%s" % (task_results[t].b_wcrt_str()))

# specify paths
p1 = s.bind_path(model.Path("P1", [t1, t2, t3, t5, t6, t7, t8, t9]))

paths = [p1]
# perform path analysis
for p in paths:
    best_case_latency, worst_case_latency = path_analysis.end_to_end_latency(p, task_results, n=1)
    print("path %s e2e latency. best case: %d, worst case: %d" % (p.name, best_case_latency, worst_case_latency))