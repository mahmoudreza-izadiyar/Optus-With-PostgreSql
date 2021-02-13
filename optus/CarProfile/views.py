import base64
import psycopg2
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cars
from .forms import CarEditForm


# ---------------------------------------------------django--model--database-------------------------------------
# Create your views here.
def index(request):
    cars = Cars.objects.all()

    context = {
        "cars": cars
    }
    return render(request, 'CarProfile/index.html', context)


def addCar(request):
    cars = Cars.objects.all()
    if request.method == 'POST' and request.FILES['photo']:
        name = request.POST.get('name')
        color = request.POST.get('color')
        model = request.POST.get('model')
        photo = request.FILES['photo']
        car = Cars.objects.create(name=name, color=color, model=model, photo=photo)

    context = {
        "cars": cars
    }
    return render(request, 'CarProfile/index.html', context)


def delete(request, carId):
    cars = Cars.objects.all()
    car = Cars.objects.get(id=carId)
    message = f"{car.name} has been deleted successfully"
    car.delete()

    context = {
        "message": message,
        "cars": cars
    }
    return render(request, 'CarProfile/index.html', context)


# Edit objects
def edit(request, carId):
    car = Cars.objects.get(id=carId)
    instance = get_object_or_404(Cars, id=carId)
    # use from to change object directly
    form = CarEditForm(request.POST or None, request.FILES, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('index')

    context = {
        'form': form,
        'car': car
    }
    return render(request, 'CarProfile/edit.html', context)


def document(request):
    return render(request, 'CarProfile/doc.html')


# -----------------------------------------------------PostgreSQL------------------------------------------------

def addByPs(request):
    if request.method == 'POST' and request.FILES['photo']:
        name = request.POST.get('name')
        color = request.POST.get('color')
        model = request.POST.get('model')
        photo = request.FILES['photo']
        #  Encoding photo to save it into the backend
        image_read = photo.read()
        photo_binary = base64.b64encode(image_read)

        conn = None
        try:

            # connect to the PostgreSQL database
            conn = psycopg2.connect(
                host="localhost",
                database="Optus",
                user="postgres",
                password="m1m2m3m4",
                port="5433")

            # create a cursor object for execution
            cur = conn.cursor()

            # Query Selector
            postgreSQL_select_Query = "SELECT * FROM  car"

            # call a stored procedure
            cur.execute(postgreSQL_select_Query)
            cars = cur.fetchall()

            # call a stored procedure
            cur.execute('CALL insert_carpost(%s,%s,%s,%s)', (name, model, color, photo_binary))

            # commit the transaction
            conn.commit()

            # close the cursor
            cur.close()

            context = {

                "message": "Your New car has been added with postgreSQL call "
            }
            return render(request, 'CarProfile/addByPs.html', context)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            context = {
                "cars": cars,
                "message": "Something Bad Happened !  505ish "
            }
            return render(request, 'CarProfile/addByPs.html', context)
        finally:
            if conn is not None:
                conn.close()
    context = {

        "message": "You can Add your car here and then you can see all of them in Cars menu"
    }
    return render(request, 'CarProfile/addByPs.html', context)




def showCar(request):
    conn = None

    try:

        # connect to the PostgreSQL database
        conn = psycopg2.connect(
            host="localhost",
            database="Optus",
            user="postgres",
            password="m1m2m3m4",
            port="5433")

        # create a cursor object for execution
        cur = conn.cursor()
        # Query Selector
        cur.execute("SELECT * FROM  car")
        # fetch all cars
        cars = cur.fetchall()
        # Cars with decoded photos
        cars_decode = []
        for car in cars:
            car_photo = base64.b64decode(car[4])
            cars_decode.append([car[0], car[1], car[2], car[3], car_photo])

        # send cars to template
        context = {
            "cars_decode": cars_decode,
            "cars": cars,
            "message": "Have a look to your terminal "
        }
        return render(request, 'CarProfile/showCar.html', context)
    # Error Handling
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        context = {

            "message": "Something Bad Happened !  505ish "
        }
        return render(request, 'CarProfile/showCar.html', context)
    finally:
        if conn is not None:
            conn.close()
        context = {
            "cars_decode": cars_decode,
            "cars": cars,

        }
        return render(request, 'CarProfile/showCar.html', context)


# Delete car Rows with execute postgresql command
def deleteCar(request, carId):
    conn = None
    try:

        # connect to the PostgreSQL database
        conn = psycopg2.connect(
            host="localhost",
            database="Optus",
            user="postgres",
            password="m1m2m3m4",
            port="5433")

        # create a cursor object for execution
        cur = conn.cursor()

        # execute delete command inside the posgresql
        cur.execute(f"DELETE FROM car WHERE id= {carId}")
        conn.commit()

        # fetch new database and show it in template
        cur.execute("SELECT * FROM  car")
        cars = cur.fetchall()
        # decode photos and add them to new list to send for template
        cars_decode = []
        for car in cars:
            car_photo = base64.b64decode(car[4])
            cars_decode.append([car[0], car[1], car[2], car[3], car_photo])

        context = {
            "cars": cars,
            "message": f"{car[0]} Has been deleted successfully! "
        }
        return render(request, 'CarProfile/showCar.html', context)
    # Error Handling
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        context = {
            "message": f"Something Bad Happened !  505ish \n {error} "
        }
        return render(request, 'CarProfile/showCar.html', context)
    finally:
        if conn is not None:
            conn.close()
        context = {
            "cars_decode": cars_decode,
            "cars": cars,

        }
        return render(request, 'CarProfile/showCar.html', context)


def editCar(request, carId):
    # connect to the PostgreSQL database
    conn = psycopg2.connect(
        host="localhost",
        database="Optus",
        user="postgres",
        password="m1m2m3m4",
        port="5433")

    # create a cursor object for execution
    cur = conn.cursor()
    # execute SELECT command inside the posgresql
    cur.execute(f"SELECT * FROM car WHERE id= {carId}")
    car = cur.fetchall()

    if request.method == 'POST' and request.FILES['photo']:
        name = request.POST.get('name')
        color = request.POST.get('color')
        model = request.POST.get('model')
        photo = request.FILES['photo']
        #  Encoding photo to save it into the backend
        image_read = photo.read()
        photo_binary = base64.b64encode(image_read)

        cur.execute('CALL update_car(%s,%s,%s,%s,%s)', (carId, name, model, color, photo_binary))
        conn.commit()
        # Show new with new data
        cur.execute(f"SELECT * FROM car WHERE id= {carId}")
        car = cur.fetchall()

        context = {
            "car": car
        }
        return render(request, 'CarProfile/editCar.html', context)

    context = {
        "car": car,
        "message": "edit cars "
    }
    return render(request, 'CarProfile/editCar.html', context)
