class Sputnik.MainMenu extends Backbone.View
  id: 'main-menu'
  className: 'menu-animation'
  events:
    'click #menu-config': 'showConfig'

  initialize: ->
    @template = Sputnik.loadTemplate('mainMenu')

  render: ->
    @$el.html(@template())

  showConfig: (e) =>
    @$el.removeClass('menu-animation')
