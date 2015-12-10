class Sputnik.Login extends Backbone.View
  id: 'wrap'
  events:
    'keypress input': 'onKeyPress'
    'click #keep-signin': 'toggleKeep'
    'click #login-btn': 'attemptLogin'

  initialize: ->
    @template = Sputnik.loadTemplate('login')

  render: ->
    @$el.html(@template())

  onKeyPress: (e) =>
    code = e.keyCode || e.which
    if code == 13
      @attemptLogin()

  toggleKeep: =>
    @$el.find('#keep-signin').toggleClass('active')

  attemptLogin: =>
    data = {
      username: @$el.find('#username').val()
      password: @$el.find('#password').val()
      keep_signed: @$el.find('#keep-signin').hasClass('active')
    }
    console.log('Mock login', data)
    animationEvents = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend'
    @$el.one(animationEvents, @hideLogin)
    @$el.find('input').prop('disabled', true)
    @$el.addClass('animated fadeOut')

  hideLogin: (e) ->
    console.log(e)