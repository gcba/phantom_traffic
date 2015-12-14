class Sputnik.MainMenu extends Backbone.View
  id: 'main-menu'
  className: 'menu-intro-animation'
  events:
    'click #menu-config': 'showConfig'

  initialize: ->
    @template = Sputnik.loadTemplate('mainMenu')

  render: ->
    @$el.html(@template())

  showConfig: =>
    @$el.removeClass('menu-intro-animation').addClass('menu-outro-animation')
