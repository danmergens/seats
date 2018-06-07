from flask import Flask, request, make_response, jsonify, abort


app = Flask(__name__)
# For now, we use in memory, actual code would use NoSQL database to store.
events = []


#####
# Data functions - global
#####
def event_ids():
    return [x['event_id'] for x in events]


def event_exists(event_id):
    return event_id in event_ids()


def get_event_by_id(event_id):
    if event_exists(event_id):
        return [x for x in events if x['event_id'] == event_id][-1]
    return None


def seat_ids(event_id):
    if event_exists(event_id):
        event = get_event_by_id(event_id)
        return [x['seat_id'] for x in event['seats']]
    return None


def seat_exists(event_id, seat_id):
    return seat_id in seat_ids(event_id)


def get_seat_by_id(event_id, seat_id):
    if seat_exists(event_id, seat_id):
        event = get_event_by_id(event_id)
        return [x for x in event.seats if x['seat_id'] == seat_id][-1]
    return None


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/events', methods=['POST'])
def create_event():
    """
    Create an event (returns a unique event id).
    :return:  Unique event id.
    """
    event_id = 1
    if events:
        event_id = events[-1]['event_id'] + 1
    events.append({'event_id': event_id, 'seats': []})
    return jsonify(events[-1])


@app.route('/events', methods=['GET'])
def get_events():
    """
    Find available events.
    Request may contain the following parameters:
    - verbose: If true, returns all info for all events, otherwise, only the event ids are returned.
    """
    verbose = False
    if request.json:
        verbose = request.json.get('verbose', False)

    if verbose:
        return jsonify(events)
    return jsonify(event_ids())


@app.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    """
    Find available events.
    Request may contain the following parameters:
    :returns:  Full details of the event.
    """
    event = get_event_by_id(event_id)

    if not event:
        print 'invalid event id: %r' % event_id
        abort(404)

    return jsonify(event)


@app.route('/events/<int:event_id>/seats/<seat_id>', methods=['POST'])
def create_seat(event_id, seat_id):
    """
    Given an event, create a seat with specified parameters.
    :return:  Unique seat id for the unique event.
    """
    if not event_exists(event_id):
        abort(404, 'invalid event_id')

    event = get_event_by_id(event_id)
    if seat_exists(event_id, seat_id):
        abort(400, 'cowardly failing to create duplicate seat')

    seat_type = 'adult'
    aisle = False
    available = True

    if request.json:
        seat_type = request.json.get('type', 'adult')
        aisle = request.json.get('aisle', False)
        available = request.json.get('available', True)

    seat = {
        'seat_id': seat_id,
        'type': seat_type,
        'aisle': aisle,
        'available': available
    }
    event['seats'].append(seat)

    return jsonify(seat)


@app.route('/events/<int:event_id>/seats', methods=['GET'])
def get_seats(event_id):
    """
    Returns seats for an event.
    If parameters are specified, seats will be filtered, otherwise all seats are returned.
    Parameters:
    - available: True or False
    - type: 'child' or 'adult'
    - aisle: True or False
    :return:  JSON object with seat listing
    """
    if event_id not in [x['event_id'] for x in events]:
        print '%d not in events: %r' % (event_id, [x['event_id'] for x in events])
        abort(404, 'invalid event_id')

    seats = [x['seats'] for x in events if x['event_id'] == event_id][-1]

    if not request.json:
        return jsonify(seats)

    seat_type = request.json.get('type', None)
    aisle = request.json.get('aisle', None)

    if seat_type is not None or aisle is not None:
        return jsonify([x['seat_id'] for x in seats
                        if x['available'] and x['type'] == seat_type and x['aisle'] == aisle])
    return jsonify([x['seat_id'] for x in seats if x['available']])


if __name__ == '__main__':
    app.run(debug=True)
