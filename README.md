## Automatización de Gestión de "Liked Songs" en Spotify

Este script es una automatización propia que he desarrollado para facilitar la gestión de mi biblioteca en Spotify. La idea es eliminar de la lista "Liked Songs" aquellas canciones que ya están presentes en alguna de mis playlists, o aquellas canciones cuyos álbumes ya tengo guardados en mi biblioteca. Con ello, evito duplicados y mantengo la lista de canciones favoritas más organizada. Decidí compartirlo por aquí por si a alguno le resulta útil, ya que son automatizaciones bien específicas que no exiten herramientas ya creadas para ello.  

**Funcionalidades**

El script ofrece tres opciones principales:  

 -  Elimina de "Liked Songs" todas las canciones que ya aparecen en cualquiera de tus playlists.  
 - Elimina de "Liked Songs" aquellas canciones cuyos álbumes ya están guardados en tu biblioteca.
 - Ejecuta ambas opciones: Primero elimina las canciones que están en alguna playlist y, tras actualizar la lista de "Liked Songs", elimina aquellas cuyo álbum    esté guardado.

**Requisitos**

 - Python 3.x
 - Spotipy: Puedes instalar esta biblioteca utilizando pip:

    pip install spotipy

 - Credenciales de Spotify Developer:
 1. client_id 
 2. client_secret 
 3. redirect_uri

> Nota: Recomiendo utilizar http://127.0.0.1:8888/callback en lugar
> de localhost para evitar advertencias.

**Configuración**

 - Clona o descarga el repositorio donde se encuentra el script.
 - Reemplaza los valores de client_id y client_secret con tus propias credenciales obtenidas en Spotify Developer Dashboard.

**Uso**

 - Abre una terminal, navega hasta el directorio donde se encuentra el script y ejecuta:

    python nombre_del_script.py

 - Selecciona la opción deseada:

*Opción 1: Eliminar canciones en "Liked Songs" que estén en alguna playlist.
Opción 2: Eliminar canciones en "Liked Songs" cuyo álbum esté guardado.
Opción 3: Ejecutar ambas opciones.*
  
**Advertencia**

 - Asegúrate de que realmente deseas eliminar estas canciones de tu
   biblioteca, ya que esta acción no es reversible mediante el script.

 - Se recomienda probar el script en un entorno controlado antes de
   ejecutarlo en tu cuenta principal.
