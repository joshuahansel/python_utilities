from Animator import Animator
from MOOSEXML import readMOOSEXML

data = readMOOSEXML('safe30.xml')

ani = Animator(2, 2)
ani.nextSubplot('$z$', 'Pressure')
ani.addSet(data['mat_props_vpp']['x'], data['mat_props_vpp']['p_liquid'], '$p_\\ell$')
ani.addSet(data['mat_props_vpp']['x'], data['mat_props_vpp']['p_vapor'], '$p_v$')
ani.nextSubplot('$z$', 'Velocity')
ani.addSet(data['mat_props_vpp']['x'], data['mat_props_vpp']['vel_liquid'], '$u_\\ell$')
ani.addSet(data['mat_props_vpp']['x'], data['mat_props_vpp']['vel_vapor'], '$u_v$')
ani.nextSubplot('$z$', 'Void Fraction', pad=True)
ani.addSet(data['mat_props_vpp']['x'], data['mat_props_vpp']['alpha_vapor'], '$\\alpha_v$')
ani.addSet(data['mat_props_vpp']['x'], data['mat_props_vpp']['alpha_vapor_base'], '$\\alpha_v^{wick,i,0}$')
ani.addSet(data['mat_props_vpp']['x'], data['mat_props_vpp']['alpha_vapor_max_i'], '$\\alpha_v^{wick,i,+}$')
ani.addSet(data['mat_props_vpp']['x'], data['mat_props_vpp']['alpha_vapor_max_o'], '$\\alpha_v^{wick,o,+}$')
ani.nextSubplot('$z$', 'Temperature')
ani.addSet(data['mat_props_vpp']['x'], data['mat_props_vpp']['T_liquid'], '$T_\\ell$')
ani.addSet(data['mat_props_vpp']['x'], data['mat_props_vpp']['T_vapor'], '$T_v$')
ani.addSet(data['mat_props_vpp']['x'], data['mat_props_vpp']['T_int'], '$T_{int}$')
ani.addSet(data['mat_props_vpp']['x'], data['mat_props_vpp']['T_wall'], '$T_{wall}$')
ani.show()
