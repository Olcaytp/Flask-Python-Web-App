from flask import Flask, jsonify, request, abort

app = Flask(__name__)

tasks = []

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/tasks', methods=['POST'])
def add_task():
    if not request.json or 'title' not in request.json:
        abort(400)
    task = {
        'id': len(tasks) + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)
