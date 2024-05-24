Para poner a funcionar el código del proyecto de sistemas distribuidos, toca correr los código por cada capa, entonces

CAPA EDGE
Para poder a funcionar cualquier aspersor solo hace falta ingresar a la carpeta de sensors y ahí seleccionar el sensor deseado.
Para poner a funcionar el sistema de calidad, hay que ingresar a la capa de sensors y poner a correr el sistema de calidad(quality_system).

CAPA FOG
Para poner a funcionar el contenido de esta capa hay que correr: 
-el proxy (receptor_fog)
-el health check (health_check)
-el sistema de calidad(quality_system)

El proxy debe correr antes que el health check porque de otra forma, el health check activará el respaldo del proxy.

CAPA CLOUD
Para hacer que esta capa funcione hay que correr:

- el proxy de esta capa (cloud_proxy)
- calculadora del promedio mensual de la humedad (humidity_calculation)
- el sistema de calidad(quality_system)

en este caso el orden no importa porque el sistema de calidad espera al proxy y el promedio mensual de la humedad lo hace con el archivo json de lo cloud.


Lo mejor seria correr el sensor de la capa edge de ultimo para asegurar que lleguen todos los datos. 
