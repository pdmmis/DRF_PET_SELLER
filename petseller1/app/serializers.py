from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class Categoryserializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AnimalBreedserializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalBreed
        # fields = '__all__'
        fields = ['animal_breed']



class Animalcolorserializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalColors
        # fields = '__all__'
        fields = ['animal_color']

class AnimalImageserializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalImages
        fields = '__all__'



class Animalserializer(serializers.ModelSerializer):
    animal_category=serializers.SerializerMethodField()  #Categoryserializer()
    animal_color=Animalcolorserializer(many=True)
    animal_breed=AnimalBreedserializer(many=True)
    animal_image=AnimalImageserializer(many=True)

    def get_animal_category(self,obj):
        return obj.animal_category.category_name
    

    # def to_representation(self, instance):
    #     animal_color_serializer=Animalcolorserializer(instance.animal_color.all(),many=True)
    #     payload={
    #         'animal_category':instance.animal_category.category_name,
    #         'animal_name':instance.animal_name,
    #         'animal_views':instance.animal_views,
    #         'animal_likes':instance.animal_likes,
    #         'animal_description':instance.animal_description, 
    #         'animal_color':animal_color_serializer.data    
    #     }
    #     return payload
    def create(self,data):
        animal_breed=data.pop('animal_breed')
        animal_color=data.pop('animal_color')
        animal=Animal.objects.create(**data,animal_category=Category.objects.get(category_name="dog"))
        for ab in animal_breed:
            animal_breed_obj=AnimalBreed.objects.get(animal_breed=ab['animal_breed'])
            animal.animal_breed.add(animal_breed_obj)

        for ac in animal_color:
            animal_color_obj=AnimalColors.objects.get(animal_color=ac['animal_color'])
            animal.animal_color.add(animal_color_obj)
        return Animal.objects.first()
    
    def update(self,instance,data):
        if 'animal_breed' in data:
            animal_breed=data.pop('animal_breed')
            instance.animal_breed.clear()
            for ab in animal_breed:
                animal_breed_obj=AnimalBreed.objects.get(animal_breed=ab['animal_breed'])
                instance.animal_breed.add(animal_breed_obj)

        if 'animal_color' in data:
            animal_color=data.pop('animal_color')
            instance.animal_color.clear()
            for ac in animal_color:
                animal_color_obj=AnimalColors.objects.get(animal_color=ac['animal_color'])
                instance.animal_color.add(animal_color_obj)


        instance.animal_name=data.get('animal_name',instance.animal_name)
        instance.animal_description=data.get('animal_description',instance.animal_description)
        instance.animal_gender=data.get('animal_gender',instance.animal_gender)
        instance.save()
        return instance





    class Meta:
        model = Animal
        # fields = '__all__'
        exclude=['updated_at','created_at']

class AnimalLocationserializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalLocation
        fields = '__all__'



class RegisterSerializer(serializers.Serializer):
    username=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField()

    def validate(self, data):
        if 'username' in data:
            user=User.objects.filter(username=data['username'])
            if user.exists():
                raise serializers.ValidationError('username is already taken')
    
        if 'email' in data:
                user=User.objects.filter(email=data['email'])
                if user.exists():
                    raise serializers.ValidationError('email is already taken')
        return data
    
class LoginSerialzer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
    def validate(self,data):
        if 'username' in data:
            user=User.objects.filter(username=data['username'])
            if not user.exists():
                raise serializers.ValidationError('username not exists')
        # if 'password' in data:
        #     user=User.objects.filter(username=data['password'])
        #     if not  user.exists():
        #         raise serializers.ValidationError('password not matched')
        return data    