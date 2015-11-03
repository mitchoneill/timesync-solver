import pika
import json
from timesyncsolver.solver import Teachers, Subjects, TimeSlots, Solver


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='solver')


def on_request(ch, method, props, req):
    req_json = json.loads(req)

    teachers = Teachers()
    teachers.add(req_json['teachers'])
    subjects = Subjects()
    subjects.add(req_json['subjects'])
    timeslots = TimeSlots(req_json['timeslots'])

    solver = Solver(teachers, subjects, timeslots)
    solver.solve()

    response = solver.solution

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(
                         correlation_id=props.correlation_id
                     ),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='solver')


channel.start_consuming()
