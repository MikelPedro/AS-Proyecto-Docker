# AS-Proyecto-Docker
Pagina web para buscar la temperatura de tu ciudad.
El codigo esta disponible en la rama **master**.

```bash
git clone -b master <url-repositorio>
```
## Docker

Posicionarse en la carpeta entregadocker

```bash
cd entregadocker
```
Hacer docker compose

```bash
sudo docker compose up
```
## Ir al navegador y poner la IP de la instancia, si no va entonces poner IP:80/
## Kubernetes

Posicionarse en la carpeta del repositorio

Iniciar minikube

```bash
minikube start
```

```bash
kubectl apply -f kubernetes/
```

```bash
minikube tunnel
```
