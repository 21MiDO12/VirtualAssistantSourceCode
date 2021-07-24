import modules as m

m.OnPrelaunch()

m.OnLaunch().launch()
print(m.f.getToDayEvents(0))
m.OnRun().start()
