from transitions.extensions.nesting import NestedState
from transitions.extensions import MachineFactory

# create a machine with mixins
async_nested = MachineFactory.get_predefined(asyncio=True, nested=True)
NestedState.separator = '↦'

states_eng = ['undefined',
              {'name': 'small', 'children': ['cash', 'card']},
              {'name': 'big', 'children': ['cash', 'card']},
              'confirmed'
              ]

transitions_eng = [
    ['reset', '*', 'undefined'],
    ['reset_payment', ['big↦cash', 'big↦card'], 'big'],
    ['reset_payment', ['small↦cash', 'small↦card'], 'small'],
    ['cash', ['small', 'small↦card'], 'small↦cash'],
    ['cash', ['big', 'big↦card'], 'big↦cash'],
    ['card', ['small', 'small↦cash'], 'small↦card'],
    ['card', ['big', 'big↦cash'], 'big↦card'],
    ['big', ['small', 'undefined'], 'big'],
    ['big', 'small↦cash', 'big↦cash'],
    ['big', 'small↦card', 'big↦card'],
    ['small', ['big', 'undefined'], 'small'],
    ['small', 'big↦cash', 'small↦cash'],
    ['small', 'big↦card', 'small↦card'],
    ['accept', '*', 'confirmed']
    ]


states = ['undefined',
          {'name': 'маленькую', 'children': ['наличкой', 'картой']},
          {'name': 'большую', 'children': ['наличкой', 'картой']},
          'confirmed'
          ]


transitions = [
    ['reset', '*', 'undefined'],
    ['reset_payment', ['большую↦наличкой', 'большую↦картой'], 'большую'],
    ['reset_payment', ['маленькую↦наличкой', 'маленькую↦картой'], 'маленькую'],
    ['наличкой', ['маленькую', 'маленькую↦картой'], 'маленькую↦наличкой'],
    ['наличкой', ['большую', 'большую↦картой'], 'большую↦наличкой'],
    ['картой', ['маленькую', 'маленькую↦наличкой'], 'маленькую↦картой'],
    ['картой', ['большую', 'большую↦наличкой'], 'большую↦картой'],
    ['большую', ['маленькую', 'undefined'], 'большую'],
    ['большую', 'маленькую↦наличкой', 'большую↦наличкой'],
    ['большую', 'маленькую↦картой', 'большую↦картой'],
    ['маленькую', ['большую', 'undefined'], 'маленькую'],
    ['маленькую', 'большую↦наличкой', 'маленькую↦наличкой'],
    ['маленькую', 'большую↦картой', 'маленькую↦картой'],
    ['accept', '*', 'confirmed']
    ]
