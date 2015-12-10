class Sputnik.Header extends Backbone.View
  id: 'header'

  initialize: ->
    @template = Sputnik.loadTemplate('header')

  render: ->
    @$el.html(@template())