
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

- ### Uso sencillo

    Una de las características de FastAPI es que genera documentación de cada una de las rutas definidas de forma automática, facilitando así el uso de la API a los clientes de esta. 

    &nbsp;
	![Imagen de la documentación de la API](assets/imagen-docs.png)

- ### Autenticación mediante Google API

    La API es totalmente segura, ya que en ningún momento tiene acceso a información sensible. Esto se debe a que la autenticación se realiza en los servidores seguros de Google. La única información a la que se tiene acceso es el e-mail, con el que se verifica la identidad del profesor que intenta usar la API. 

    &nbsp;
    ![Imagen de la pantalla de login de Google](assets/imagen-google-login.png)

- ### Autorización con tokens JWT

    Una vez el profesor se identifica, se le concede un token JWT firmado por el servidor con el que podrá demostrar su identidad en las futuras peticiones que realice.
    
    Este token también se usa para validar los roles del profesor cuando intenta acceder a rutas restringidas. 

    ```json
    {"access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJBTFAiLCJleHAiOjE2NTU0MTEyMzN9.S_YPiRapP_v3dCCn4OdR0Iy8QC_CtMo4-BD7OTExeAU", "token_type": "bearer"}
    ```

    [![](http://jwt.io/img/badge.svg)](https://jwt.io/)


## Requisitos

Es necesario tener Python 3.10 instalado.	

## Guía de instalación

1. Ejecuta el siguiente comando desde el terminal:
	
    ```shell
    git clone https://github.com/alp09/api-horario.git
    ```

* También puedes descargar el código fuente desde este [enlace](https://github.com/alp09/api-horario/archive/refs/heads/main.zip).


2. A continuación instala el proyecto y sus dependencias con el comando:

    ```shell
    pip install -e .
    ```

* También tendrás que instalar el driver de la base de datos que decidas usar. La lista completa de drivers admitidos la puedes encontrar en la [documentación de SQLAlchemy](https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls).


* En caso de que vayas a ejecutar los test necesitarás las dependencias de desarrollo. Para instalarlas usa el comando:

    ```shell
    pip install -r requirements-dev.txt
    ```

## Configuración

Los archivos de configuración del proyecto se encuentran bajo el paquete `config`. Aquí encontrarás dos archivos:

* `cliente_secret.json` es un archivo proporcionado por Google al registrar un proyecto como cliente de las API de Google. Puedes encontrar más información en el [tutorial de Google](https://developers.google.com/identity/sign-in/web/sign-in). Si necesitas una guía paso a paso la puedes encontrar en los [docs del repositorio](https://docs.google.com/viewer?url=https://github.com/alp09/api-horario/raw/main/docs/Configuraci%C3%B3n%20del%20cliente%20de%20Google.pdf).


* `settings.py` es el archivo de configuración principal. Aquí podrás modificar la dirección de la API, indicar la URL de tu base de datos, etc. Tienes una guía detallada en los [docs del repositorio](https://docs.google.com/viewer?url=https://github.com/alp09/api-horario/raw/main/docs/Configuraci%C3%B3n%20de%20la%20API.pdf).
