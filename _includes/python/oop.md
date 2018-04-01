
Python, being a multi-paradigm programming language, supports different programming approach. Common programming paradigms include:
* Object-oriented
* Functional
* etc.

I summarised Object-oriented programming (OOP) and their fundamental concepts with examples in Python3 in this post. For [Functional programming in Python3](https://www.kdnuggets.com/2018/02/introduction-functional-programming-python.html), you may find [this post](https://www.kdnuggets.com/2018/02/introduction-functional-programming-python.html) useful.


## Object-oriented programming (OOP)

The key concept of OOP is to create sharable classes so that codes can be reused. Data are secure with data abstraction.

### What are class & object in Python?

A class is the blueprint for the object, it is a collection of data (variables) and methods (functions). An object is an instantiation of a class. We can create multiple objects from a class.

A new instance is created in memory here and the age binds with it.

We can delete `obj` using `del` 


```python
del obj
```

Then the name `obj` is removed from the corresponding namespace. However, the object still exists in memory. When no other name bounds with it, that is to say, it becomes an unreferenced object, python automatically destroys it. And this is called garbage collection. We can also force it using:


```python
gc.collect()
```

### Methods

Methods are functions defined inside of a class. They are used to define the behavior of an object.

The goal of OOP is to produce reusable code and reduce redundant ones.

To achieve this goal, we utilise 3 basic concepts:

* __Inheritance__

* __Encapsulation__

* __Polymorphism__


## Inheritance

A process of creating a child class for using functions of an existing one without modifying it.

`super()` is used before `__init__()` to pull the content of `__init__()` method from the parent class into the new one.

#### Multiple inheritance

A class can be derived from more than one base classes:

#### Multilevel inheritance

Similarly, a class can inherit from a derived class.

This is called multilevel inheritance. You can go into any depth. Python searches a specified attribute in the current class first. If not found, the search process continues into parent classes in a depth-first, left-right manner. Such rule is called Method Resolution Order (MRO). Python offers `mro()` method for checking.


```python
MultiDerived.mor()
```

## Encapsulation

In Python, we denote private attribute using single or double underscores as prefix to prevent attributes from being modified directly. Such access restriction on methods or variables is called encapsulation.


## Polymorphism

When two classes have a common method with different functions, we can create a common interface that can take any object to handle different data types more efficiently.
