# API Documentation

## Endpoints:

### `GET /tasks`

Returns a list of tasks.

```
> GET /tasks

< 200 OK
{
  tasks: Task[] = [
    { id: number, label: string, completed: boolean, parent_task: number | null }
  ]
}
```

### `GET` /tasks/:id
Return a list of sub tasks of task with given ID
```
> GET /tasks/1

< 200 OK
{
  tasks: Task[] = [
    { id: number, label: string, completed: boolean, parent_task: number | null }
  ]
}
```

### `POST /tasks`

Creates a new task.
If parent task id is specified it creates a sub task
```
> POST /tasks
{ label: string } |
{ label: string, parent_task: number }

< 201 Created
{
  task: { id: number, label: string, completed: boolean, parent_task: number | null }
}
```

### `POST /tasks/:id`

Updates the task of the given ID.

```
> POST /tasks/:id
{ label: string } |
{ completed: boolean } |
{ label: string, completed: boolean }

< 200 OK
{
  task: Task = { id: number, label: string, completed: boolean, parent_task: number | null }
}

< 404 Not Found
{ error: string }
```

### `DELETE /tasks/:id`

Deletes the task of the given ID.

```
> DELETE /tasks/:id

< 204 No Content

< 404 Not Found
{ error: string }
```