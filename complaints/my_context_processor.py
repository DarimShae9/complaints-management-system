def my_cp(request):
    user = request.user
    ctx = {}
    if user.is_authenticated:
        ctx.update({
            'current_user': user
        })
    return ctx
