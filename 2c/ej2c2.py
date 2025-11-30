"""
Enunciado:
Desarrolla una API REST utilizando Flask que permita realizar operaciones básicas sobre una lista de tareas (to-do list).
La API debe exponer los siguientes endpoints:

1. `GET /tasks`: Devuelve la lista completa de tareas.
2. `POST /tasks`: Agrega una nueva tarea. El cuerpo de la solicitud debe incluir un JSON con el campo "name".
3. `DELETE /tasks/<task_id>`: Elimina una tarea específica por su ID.
4. `PUT /tasks/<task_id>`: Actualiza el nombre de una tarea existente por su ID. El cuerpo de la solicitud debe incluir un JSON con el campo "name".

Observa que el mismo endpoint (por ejemplo, `/tasks/<task_id>`) puede recibir diferentes verbos HTTP (DELETE, PUT) y realizar distintas operaciones según el verbo utilizado. Esta es una característica fundamental de las APIs REST.

Requisitos:
- Cada tarea debe tener un ID único (entero) y un nombre (cadena de texto).
- La lista de tareas debe almacenarse en memoria (no es necesario usar una base de datos).
- Maneja errores como intentar eliminar o actualizar una tarea que no existe.

Ejemplo:
Si la lista de tareas inicial está vacía:
1. Una solicitud `POST /tasks` con el cuerpo `{"name": "Comprar leche"}` debe agregar la tarea con ID 1.
2. Una solicitud `GET /tasks` debe devolver `[{"id": 1, "name": "Comprar leche"}]`.
3. Una solicitud `PUT /tasks/1` con el cuerpo `{"name": "Comprar pan"}` debe actualizar la tarea con ID 1.
4. Una solicitud `GET /tasks` debe devolver `[{"id": 1, "name": "Comprar pan"}]`.
5. Una solicitud `DELETE /tasks/1` debe eliminar la tarea con ID 1.
6. Una solicitud `GET /tasks` debe devolver `[]`.

Tu tarea es implementar esta API en Flask.
"""

from flask import Flask, jsonify, request

# Esta lista almacenará todas las tareas
tasks = []
# Este contador se usará para asignar IDs únicos
next_id = 1

def create_app():
    """
    Crea y configura la aplicación Flask
    """
    app = Flask(__name__)

    @app.route('/tasks', methods=['GET'])
    def get_tasks():
        """
        Devuelve la lista completa de tareas
        """
        # Implementa este endpoint
        return jsonify(tasks), 200

    @app.route('/tasks', methods=['POST'])
    def add_task():
        """
        Agrega una nueva tarea
        El cuerpo de la solicitud debe incluir un JSON con el campo "name"
        """
        # Implementa este endpoint
        global next_id, tasks

        data = request.get_json(silent=True) or {}
        name = data.get("name")

        if not name:
            # Petición mal formada
            return jsonify({"error": "Field 'name' is required"}), 400

        task = {"id": next_id, "name": name}
        tasks.append(task)
        next_id += 1

        # 201 Created tiene sentido para POST que crea recursos
        return jsonify(task), 201

    @app.route('/tasks/<int:task_id>', methods=['DELETE'])
    def delete_task(task_id):
        """
        Elimina una tarea específica por su ID
        """
        global tasks

        for i, task in enumerate(tasks):
            if task["id"] == task_id:
                tasks.pop(i)
                return jsonify({"message": "Task deleted"}), 200

        # No encontrada
        return jsonify({"error": "Task not found"}), 404

    @app.route('/tasks/<int:task_id>', methods=['PUT'])
    def update_task(task_id):
        """
        Actualiza el nombre de una tarea existente por su ID
        El cuerpo de la solicitud debe incluir un JSON con el campo "name"
        Código de estado: 200 - OK si se actualizó, 404 - Not Found si no existe
        """
        data = request.get_json(silent=True) or {}
        name = data.get("name")

        if not name:
            return jsonify({"error": "Field 'name' is required"}), 400

        for task in tasks:
            if task["id"] == task_id:
                task["name"] = name
                return jsonify(task), 200

        return jsonify({"error": "Task not found"}), 404

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)