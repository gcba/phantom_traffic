class Sputnik.Login extends Backbone.View
  id: 'wrap'
  events:
    'keypress input': 'onKeyPress'
    'click #keep-signin': 'toggleKeep'
    'click #login-btn': 'attemptLogin'

  initialize: ->
    @template = Sputnik.loadTemplate('login')

  render: (fall=true) ->
    @$el.html(@template())
    if fall
      @$el.addClass('fall')
      @$el.one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', =>
        @$el.removeClass('fall')
      )

  onKeyPress: (e) =>
    code = e.keyCode || e.which
    if code == 13
      @attemptLogin()

  toggleKeep: =>
    @$el.find('#keep-signin').toggleClass('active')

  attemptLogin: =>
    # TODO: sign in de verdad
    data = {
      username: @$el.find('#username').val()
      password: @$el.find('#password').val()
      keep_signed: @$el.find('#keep-signin').hasClass('active')
    }
    user = {
      username: 'iheredia'
      name: 'Ignacio'
      surname: 'Heredia'
      img: '/static/imgs/users/iheredia.png'
    }
    console.log('Mock login', data)
    console.log('Mock user', user)

    @$el.find('input').prop('disabled', true)
    animationEvents = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend'
    @$el.one(animationEvents, => @trigger('userSignedIn', user))
    @$el.addClass('animated fadeOut')
