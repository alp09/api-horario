
# API de reservas

[![Tests](https://github.com/alp09/api-horario/actions/workflows/tests.yml/badge.svg)](https://github.com/alp09/api-horario/actions/workflows/tests.yml)

---

## Introducción

Este es el BackEnd de mi proyecto final del CFGS Desarrollo de Aplicaciones Multiplataformas.

El proyecto que me fue asignado trata de una aplicación que permita a los profesores de [mi instituto](http://www.iestorredelrey.es/es/) ver el horario de clases y realizar reservas de aulas. Los profesores podrán acceder a dicha aplicación mediante las cuentas corportivas de Google.

También debe permitir a unos profesores administradores insertar los datos de asignaturas, aulas, horarios, etc. al comienzo de cada año lectivo, además de gestionar las reservas que hacen el resto de sus compañeros.  


## Tecnologías

* **[FastAPI](https://github.com/tiangolo/fastapi)** : un web framework de Python para programar APIs. Lo elegí más tarde en el desarrollo por su facilidad de uso y soporte para validación de datos.  


* **[Pydantic](https://github.com/samuelcolvin/pydantic)** : una librería de validación de datos que usa el sistema de type-hints de Python para forzar los tipos de variables durante la ejecución del programa. Es usada por FastAPI para validar los datos entrantes y salientes de las rutas de la API. 


* **[SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy)** : es un toolkit de SQL y ORM de Python.   


* **[SQLModel](https://github.com/tiangolo/sqlmodel)** : es un wrapper de Pydantic y SQLAlchemy cuyo objetivo es facilitar el desarrollo de aplicaciones FastAPI.


* **[Google API client](https://github.com/googleapis/google-api-python-client)** : es el cliente proporcionado por Google para consumir las distintas API que proveen. 


* **[PyJWT](https://github.com/jpadilla/pyjwt)** : una librería de Python para codificar y decodificar tokens JWT.




## Features

- ### Autenticación mediante Google API

    La API es totalmente segura, ya que en ningún momento tiene acceso a información sensible. Esto se debe a que la autenticación se realiza en los servidores seguros de Google. La única información a la que se tiene acceso es el e-mail, con el que se verifica la identidad del profesor que intenta usar la API. 

    &nbsp;
    ![Imagen de la pantalla de login de Google](https://user-images.githubusercontent.com/65811900/173885934-423fab9c-8dbc-44e9-bc06-b0247a804503.png)

- ### Autorización con tokens JWT

    Una vez el profesor se identifica, se le concede un token JWT firmado por el servidor con el que podrá demostrar su identidad en las futuras peticiones que realice.
    
    Este token también se usa para validar los roles del profesor cuando intenta acceder a rutas restringidas. 

    ```json
    {"access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjb2RpZ28iOiJBTFAiLCJlbWFpbCI6ImFiZWxscDEzQGdtYWlsLmNvbSIsIm5vbWJyZSI6IkxcdTAwZjNwZXogUGFycmFkbywgQWJlbCIsImVzX2FkbWluIjp0cnVlLCJleHAiOjE2NTUzMjAwOTh9.CpQYLHpWTTq1Xqt8BtDtNcurmKI4etgzOfB4MC54ux0"}
    ```

    Pruebalo [aquí](https://jwt.io/).

- ### Uso sencillo

    Una de las características de FastAPI es que genera documentación de cada una de las rutas definidas de forma automática, facilitando así para los clientes de la API el uso de esta. 




