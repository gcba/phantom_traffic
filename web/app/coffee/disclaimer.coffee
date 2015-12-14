class Sputnik.Disclaimer extends Backbone.View
  id: 'footer'

  initialize: ->
    @template = Sputnik.loadTemplate('disclaimer')

  render: (options={fadein:true}) ->
    @$el.html(@template())
    @$el.toggleClass('fadein', options.fadein)