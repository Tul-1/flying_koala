from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, Ingredient, Quantity
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    try:
        s = request.GET['send']
    except:
        s = None
    top_recipe_list = Recipe.objects.order_by('-like_number')[:5]
    #cuisines = [i.replace('+', ' ') for i in 'African American British Caribbean Chinese East+European French Greek Indian Irish Italian Japanese Korean Mexican Nordic North+African Pakistani Portuguese South+American Spanish Thai+and+South-European+Asian Turkish+and+Middle+Eastern Other'.split()]
    context = {'recipes': top_recipe_list, 's':s, 'amount':len(Recipe.objects.filter(username=request.user.username))}
    return render(request, 'homepage.html', context)

def insert_ingredient(ing):
    ingredient = Ingredient.objects.filter(ingredient_name=ing.lower())
    if len(ingredient) > 0:
        return ingredient[0]
    # for item in Ingredient.objects.all():
    #     if item.ingredient_name.lower() == ing.lower():
    #         item.recipe.add(r)
    #         return item
                    
            
    h = Ingredient(ingredient_name=ing)
    h.save()
    return h

@login_required(login_url='/signin/')
def send(request):
    logged_user = request.user

    try:
        name = request.POST['name_txt']
        description = request.POST['description']
        serves = int(request.POST['serves'])
        steps = request.POST['steps']
        ingredients = request.POST['ingredients']
        prep = request.POST['prep']
        cuisine = request.POST['cuisine']
    except:
        return redirect('/?send=fail')

    if name == '' or ingredients == '' or steps == '':
        return redirect('/?send=fail')

    ingredients = ingredients.split('\n')
    ingredients = [i.split(' ', maxsplit=1) for i in ingredients]

    r = Recipe(cuisine=cuisine, recipe_name=name, description=description, serves=serves, steps=steps, pub_date=timezone.now(), username=logged_user.username, user=logged_user, prep_time=prep)
    r.save()

    for i in ingredients:
        ing = insert_ingredient(i[1])
        if i[0] == '-':
            i2 = ''
        else:
            i2 = i[0]
        quan = Quantity(quantity=i2.replace('-', ' '), recipe=r, ingredient=ing)
        quan.save()

    return redirect('/?send=success')

def signup_login(request):
    try:
        context = {'get_return': request.GET['next'], 'amount':len(Recipe.objects.filter(username=request.user.username))}
    except:
        context = {'get_return': '/', 'amount':len(Recipe.objects.filter(username=request.user.username))}
    return render(request, 'signup_login.html', context)

def log_in(request):
    usernam = request.POST['uname']
    passwor = request.POST['pword']
    user = authenticate(username=str(usernam), password=str(passwor))
    if user is not None:
        login(request, user)
        if request.GET['next']:
            return redirect(request.GET['next'])
        return redirect('/')
    else:
        return redirect('/signin/')

def signup(request):
    usernam = request.POST['uname']
    passwor = request.POST['pword']

    for users in User.objects.all():
        if users.username == usernam:
            return redirect(f'/signin?next={request.GET["next"]}')

    a = User.objects.create_user(username=usernam, password=passwor)
    return log_in(request)

def log_out(request):
    logout(request)
    return redirect('/')

def show_recipe(request):
    logged_user = request.user

    if not logged_user.is_authenticated:
        user_exists = False
    else:
        user_exists = True

    recipe_req_id = request.GET['id']
    recipe_req = get_object_or_404(Recipe, pk=recipe_req_id)

    step = recipe_req.steps
    step_list = step.split('\n')

    liked = False
    if user_exists:
        if logged_user in recipe_req.user_likes.all():
            liked = True

    qs = Quantity.objects.filter(recipe=recipe_req_id)

    ingredients = []
    for i in qs:
        ing = Ingredient.objects.get(pk=i.ingredient.id)
        ingredients.append(f"{i.quantity.replace('-', ' ')} {ing.ingredient_name}")

    context = {'amount':len(Recipe.objects.filter(username=request.user.username)), 'recipe_req':recipe_req, 'step_list':step_list, 'liked':liked, 'ings':ingredients, 'amount':len(Recipe.objects.filter(username=request.user.username))}
    return render(request, 'show_recipe.html', context)

def profile(request):
    user_req_name = request.GET['username']
    user_req = get_object_or_404(User, username=user_req_name)
    recipes = Recipe.objects.filter(username=user_req_name)
    context = {'user_req':user_req, 'recipes':recipes, 'amount':len(recipes)}
    return render(request, 'profile.html', context)

@login_required(login_url='/signin/')
def like(request):
    logged_user = request.user

    recipe_req_id = request.GET['id']
    recipe_req = get_object_or_404(Recipe, pk=recipe_req_id)

    if logged_user in recipe_req.user_likes.all():
        recipe_req.like_number -= 1
        recipe_req.user_likes.remove(logged_user)
        recipe_req.save()
    else:
        recipe_req.like_number += 1
        recipe_req.user_likes.add(logged_user)
        recipe_req.save()

    return redirect(f'/view?id={recipe_req_id}')

def getLikeNum(recipe):
    try:
        return recipe.like_number
    except:
        return 0

def search(request):
    keywords = request.POST['keywords']
    keyword_list = keywords.split()
    results = []

    for keyword in keyword_list:
        results2 = list(Recipe.objects.filter(recipe_name__icontains=keyword))
        results2 += list(Recipe.objects.filter(description__icontains=keyword))
        x = list(Ingredient.objects.filter(ingredient_name__icontains=keyword))
        for i in x:
            try:
                results2.append(Quantity.objects.get(ingredient=i).recipe)
            except:
                pass

        for result in results2:
            if result not in results:
                results.append(result)

    results.sort(key=getLikeNum, reverse=True)

    context = {'recipes':results, 'keywords':keywords, 'amount':len(results), 'amount':len(Recipe.objects.filter(username=request.user.username))}
    return render(request, 'search_results.html', context)

@login_required(login_url='/signin/')
def delete(request):
    logged_user = request.user

    recipe_req_id = request.GET['id']
    recipe_req = get_object_or_404(Recipe, pk=recipe_req_id)

    if recipe_req.username != logged_user.username:
        raise Http404('User not matched')
    
    recipe_req.delete()

    return redirect('/')

    
    


