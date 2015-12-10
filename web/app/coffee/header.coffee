class Sputnik.Header extends Backbone.View
  id: 'header'
  className: 'animation fadeIn'

  initialize: ->
    @template = Sputnik.loadTemplate('header')

  render: ->
    @$el.html(@template())