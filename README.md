# Proyecto Final CI/CD - Numerical Analysis App

## Explicación del artefacto de software escogido
- **Propósito:** Plataforma web integral para resolver y visualizar métodos de Análisis Numérico (ecuaciones no lineales, sistemas de ecuaciones, interpolación). El objetivo es apoyar el aprendizaje y análisis mediante tablas de iteración orientadas, rastro de errores y representación gráfica.
- **Funcionalidades:** 
  - Backend: API REST construida en FastAPI (Python) exponiendo endpoints matemáticos (Algoritmos como Bisección, Newton-Raphson, Jacobi, Interpolación de Lagrange, etc.). 
  - Frontend: Single Page Application (SPA) en Vue 3 + Vite que permite al usuario interactuar de manera fluida, procesar solicitudes e ilustrar resultados de forma gráfica y modular.
- **Complejidad:** El proyecto excede una complejidad básica al tener más de dos componentes independientes: un Backend (API), un Frontend (Vue), un enrutador proxy (Nginx) y despliegue en contenedores dentro de infraestructura en la nube aprovisionada de principio a fin de manera automatizada.

## Estrategia de Versionamiento y Ramificación
Se eligió la estrategia de **Trunk-Based Development**.
- **Sustentación:** Trunk-Based fomenta la entrega e integración continua (CI/CD) al limitar el período que los desarrolladores trabajan en ramas aisladas, evitando así el "merge hell". Con esto, la rama principal (`main`) funge como el tronco único que siempre se encuentra en un estado funcional listo para liberar. Adicionalmente, esta metodología empodera al equipo a realizar iteraciones rápidas, fallar rápido, integrar sus cambios tempranamente y alinearse a la filosofía ágil de feedback constante.

## Integración de la estrategia de versionamiento a los pipelines
La convergencia de nuestro trunk principal y los flujos operan en base a los siguientes trigueros:
- **`pull_request` a `main`:** Valida la calidad estática, el linting y corre las pruebas (Unitarias / Compilación) garantizando que el merge sea confiable, sin desplegar.
- **`push` o merge a `main`:** Activa el ciclo completo. Compila código final hacia imágenes etiquetadas como *latest+sha*, inicia los análisis de Checkov y Trivy, y lanza el ciclo de aprovisionamiento de Infrastructure as Code para actualizar el cluster. Siendo trunk-based de alto nivel se incorporó como ambiente una **Aprobación Manual** final en Actions frenando la automatización productiva de un despliegue y requiriendo un ojo humano.

<img width="724" height="461" alt="image" src="https://github.com/user-attachments/assets/5238ef7b-3fab-4fd7-9349-7a5f547a79a1" />

## Diseño y Componentes del Pipeline CI/CD implementado
<img width="1502" height="684" alt="image" src="https://github.com/user-attachments/assets/5184ce44-bb47-4281-ace1-27632cdaa071" />

## Evidencia de las modificaciones o introducciones al pipeline y arquitectura
Para blindar nuestro pipeline se introdujeron cuatro características complejas:

1. **Aprobación manual para pasar a Prod:**  
   *(Se solicita aprobación en un Environment o despliegue antes de tocar Production).*
   
2. **Análisis de IaC con Checkov:**  
   *(Valida las prácticas de código de Terraform contra CIS benchmarks).*

3. **Restauración Rollback Automático y Manual:**  
   *(Permite retroceder mediante una re-aplicación de TF state con la imagen de versión que había previa a la falla si los checks no la validaron).*

4. **Análisis de Vulnerabilidades con Trivy:**  
   *(Detiene subidas con severidades CRITICAL en librerias y librerías base de OS del dockerfile).*

*Herramientas y etapas utilizadas:*
- **CI (Integración Continua):**
  - **Filtros de Ejecución (Paths):** Dispara diferentes jobs dependiendo de los cambios introducidos (Monorepo).
  - **Pruebas (Unitarias):** Pytest para Backend y Vitest para Frontend.
  - **Calidad de Código y Deuda técnica:** SonarCloud consumiendo cobertura de cobertura xml y lcov.
  - **Escaneo IaC:** **Checkov** analizando la infraestructura provista en Terraform.
- **Construcción y Registro:**
  - **Contenedores:** Generación de variables y build de Docker Images transportadas a DockerHub.
  - **Escaneo de CVEs en Contenedores:** Análisis estricto usando **Trivy** para detectar amenazas sobre las imágenes originadas.
- **CD (Despliegue Continuo):**
  - **Aprovisionamiento:** Terraform orquestando un ciclo de despliegue sobre Amazon AWS ECS. 
  - **Validaciones:** Pruebas e2e o de Humo directamente contra el balanceador de la carga productivo para determinar un "deployment state".
  - **Rollback:** Estrategia adaptada reactiva a nivel de jobs cuando se fracasa el target productivo.

## Arquitectura de Software
<img width="1093" height="823" alt="image" src="https://github.com/user-attachments/assets/01d309fe-d9ff-4ca5-a1d5-f8f21a7ba44c" />

El modelo utilizado está levantado desde cero mediante Terraform en la nube AWS:
- **Application Load Balancer (ALB):** Punto de entrada proxy que recibe el tráfico en el puerto web estándar. 
- **AWS ECS (Elastic Container Service) con modelo Fargate:** Computación *Serverless*. Dentro del clúster corre una *Task Definition* manejando bajo una misma subred tanto al contenedor de Nginx/Frontend y el contenedor FastAPI/Backend.

## Completitud y Robustez de las pruebas implementadas
La robustez se obtiene con tres capas de confirmaciones implementadas según ambiente:
1. **Pruebas Estáticas y Unitarias (Ambiente Aislado - Dockerizados):** Realizadas por Pytest y Vitest (Frontend). Validan antes que los contenedores lleguen al cloud que los outputs matemáticos de métodos complejos produzcan la divergencia o tolerancia de error adecuada según literatura matemática.
2. **Pruebas de Componente:** Realizadas en el build-time de Frontend con Cypress de forma aislada.
3. **Pruebas Smoke (Ambiente de Pre-Prod/Prod - Post-Despliegue):** Las acciones realizan peticiones `HTTP cURL` y automatizadas hacia el `alb_dns_name` generado en Terraform para confirmar conectividades de salud (`/health` y UI). Una falla dispara en el entorno la política de reversa.

## Evidencia del Pipeline ejecutado exitosamente
<img width="378" height="589" alt="image" src="https://github.com/user-attachments/assets/6b87254e-42c0-4fcb-a2d6-b9a32fdab061" />

## Socialización de desafíos y aprendizajes
- Aprendizaje de manejo de estado en Terraform y su integración con AWS S3 para mantener un estado remoto y compartido.
- Desafío de conectar FastAPI y Vue dentro de la misma Task de ECS Proxy con Nginx, requiriendo configuración detallada de puertos y rutas.
- Implementación de un pipeline robusto que no solo valide el código sino también la infraestructura y la seguridad, lo que implicó aprender a usar herramientas como Checkov y Trivy.
- La importancia de las pruebas e2e y smoke para validar el despliegue en un ambiente real antes de afectar a los usuarios finales, y cómo configurar estas pruebas dentro de GitHub Actions

# URLs de los ambientes desplegados

- [http://num-analysis-staging-alb-2119656405.us-east-1.elb.amazonaws.com/](http://num-analysis-staging-alb-2119656405.us-east-1.elb.amazonaws.com/)
- [http://num-analysis-production-alb-1607758736.us-east-1.elb.amazonaws.com/](http://num-analysis-production-alb-1607758736.us-east-1.elb.amazonaws.com/)
