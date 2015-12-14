class Sputnik.Disclaimer extends Backbone.View
  id: 'footer'

  initialize: ->
    @template = Sputnik.loadTemplate('disclaimer')

  render: (fadein=true) ->
    @$el.html(@template())
    if fadein
      @$el.addClass('fadein')