"""
file: plane_sweep.py
description: This program performs a plane sweep algorithm to solve the line
segment intersection problem and visualize it.
language: python3
author: Anurag Kallurwar, ak6491@rit.edu
"""

import sys
from enum import Enum
import bisect
# Install sortedcontainers using pip
from sortedcontainers import SortedSet
# Install matplotlib using pip
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Point:
    """
    This class holds the point coordinates and required methods
    """
    __slots__ = "x", "y"

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __hash__(self):
        return hash(self.x) + hash(self.y)

    def __str__(self):
        return "Point( {:.3f}".format(self.x) + " , {:.3f} )".format(self.y)


class Segment():
    """
    This class holds the line segment and required methods
    """
    __slots__ = "start", "end", "A", "B", "C", "key"

    def __init__(self, start, end):
        self.start = start
        self.end = end
        # Ax + By + C = 0
        self.A = start.y - end.y
        self.B = end.x - start.x
        self.C = start.x * end.y - end.x * start.y
        self.key = start

    def check_point_on_line(self, point):
        # print(str(self.A), str(self.B), str(self.C))
        if round(self.A * point.x + self.B * point.y + self.C, 5) == 0:
            if self.start.x <= point.x and point.x <= self.end.x:
                return True
        return False

    def set_key(self, key):
        self.key = key

    def __eq__(self, other):
        return (self.start == other.start) and (self.end == other.end)

    def __hash__(self):
        return hash(self.start) + hash(self.end)

    def __lt__(self, other):
        if round(other.A * self.key.x + other.B * self.key.y + other.C, 5
                 ) > 0:
            return True
        elif round(other.A * self.key.x + other.B * self.key.y + other.C, 5
                 ) == 0:
            return (-self.A / self.B) > (-other.A / other.B)
        return False

    def __str__(self):
        return "Segment: " + str(self.start) + " , " + str(self.end) + " [Key " \
               + str(self.key) + "]"


class Type(Enum):
    """
    This class holds the enumerated values for type of event
    """
    START = -1
    END = 1
    INTERSECTION = 0


class Event():
    """
    This class holds the event and required methods
    """
    __slots__ = "type", "segments", "key"

    def __init__(self, type1, segments, intersection = None):
        self.type = type1
        self.segments = segments
        self.key = intersection

    def set_key(self, intersection = None):
        if self.type == Type.START:
            self.key = self.segments[0].start
        elif self.type == Type.END:
            self.key = self.segments[0].end
        else:
            self.key = intersection

    def __eq__(self, other):
        if self.type == other.type and self.segments == other.segments:
            return True
        return False

    def __hash__(self):
        return hash(self.type) + hash(tuple(self.segments))

    def __lt__(self, other):
        if self.key.x == other.key.x:
            return self.key.y > other.key.y
        return self.key.x < other.key.x

    def __str__(self):
        output = "EVENT: type = " + str(self.type)
        # output += " | segments = [ "
        # for segment in self.segments:
        #     output += str(segment) + " ,"
        # output += " ]"
        output += " | key = " + str(self.key)
        return output


class SweepLine():
    """
    This class is the implementation for the sweep line status and required
    methods
    """
    __slots__ = "sweep_line_status"

    def __init__(self):
        self.sweep_line_status = list()

    def add(self, item):
        index = bisect.bisect_right(self.sweep_line_status, item)
        return self.sweep_line_status.insert(index, item)

    def index(self, item):
        return self.sweep_line_status.index(item)

    def get(self, index):
        return self.sweep_line_status[index]

    def remove(self, item):
        return self.sweep_line_status.remove(item)

    def swap_adjacents(self, index1, index2):
        self.sweep_line_status[index1], self.sweep_line_status[index2] = \
            self.sweep_line_status[index2], self.sweep_line_status[index1]

    def __len__(self):
        return len(self.sweep_line_status)

    def __str__(self):
        output = "=========\n"
        output += "Sweep Line Status\n"
        for current in self.sweep_line_status:
            output += str(current) + "\n"
        output += "========="
        return output


def get_intersection(line1, line2):
    """
    This Function finds interesction for two given lines
    :param line1: Segment object 1
    :param line2: Segment object 2
    :return: Point intersection
    """
    if (line1.A * line2.B - line2.A * line1.B) == 0:
        return None
    x = (line1.B * line2.C - line2.B * line1.C) / (line1.A * line2.B -
                                                   line2.A * line1.B)
    y = (line2.A * line1.C - line1.A * line2.C) / (line1.A * line2.B -
                                                   line2.A * line1.B)
    point = Point(x, y)
    if line1.check_point_on_line(point) and line2.check_point_on_line(point):
        return point
    return None


def initialize_event_queue(segments: list):
    """
    Initializes event queue with events from line segments
    :param segments: List of all the input Segment objects
    :return: event queue (SortedSet container object)
    """
    event_queue = SortedSet()
    for segment in segments:
        event = Event(Type.START, [segment])
        event.set_key()
        event_queue.add(event)
        event = Event(Type.END, [segment])
        event.set_key()
        event_queue.add(event)
    # for event in event_queue:
    #     print(event)
    return event_queue


def read_input(file_name: str):
    """
    Read input from file
    :param file_name: name of file
    :return: None
    """
    str_lines = []
    segments = []
    with open(file_name, 'r') as file:
        str_lines = file.readlines()
    number_of_segments = int(str_lines[0])
    for str_line in str_lines[1:]:
        coords = [float(a) for a in str_line.split(' ')]
        if coords[0] < coords[2]:
            segments.append(Segment(Point(coords[0], coords[1]),
                                    Point(coords[2], coords[3])))
        else:
            segments.append(Segment(Point(coords[2], coords[3]),
                                    Point(coords[0], coords[1])))
    return number_of_segments, segments


def write_output(file_name: str, intersections: list):
    """
    Write convex hull points to a file
    :param file_name: name of file
    :param intersections: intersection points
    :return: None
    """
    print("WRITING TO OUPUT FILE: " + file_name)
    with open(file_name, 'w') as file:
        file.write(str(len(intersections)) + "\n")
        for point in intersections:
            x = "{:.3f}".format(point.x)
            y = "{:.3f}".format(point.y)
            file.write(x + " " + y + '\n')


def plane_sweep(segments: list):
    """
    This method implements the plane sweep line segment algorithm to find
    intersections
    :param segments: The input line segments (list of Segment objects)
    :return: Intersection Point Objects, Order of Events happened
    """
    result = []
    print("\nINITIALIZING EVENT QUEUE...")
    event_queue = initialize_event_queue(segments)
    event_order = []
    print("\nSTARTING SWEEP LINE...")
    sweep_line_status = SweepLine()
    while len(event_queue) > 0:
        # print("\nNEW "
        #       "LOOP=======================================================\n")
        # print(sweep_line_status)
        # print("Current event queue status: ")
        # for event in event_queue:
        #     print(event)
        # print("=========")
        # print("CURRENT EVENT: ")
        current_event = event_queue.pop(0)
        event_order.append(current_event) # Saving order of events happened
        # print("=========")
        # print(current_event)
        # START EVENT
        if current_event.type == Type.START:
            # print("START======================================================")
            current = current_event.segments[0]
            sweep_line_status.add(current)
            # print(sweep_line_status)
            index = sweep_line_status.index(current)
            # print(index)
            above = None
            below = None
            if index - 1 >= 0:
                above = sweep_line_status.get(index - 1)
                intersection = get_intersection(above, current)
                # print("ADD ABOVE")
                # print(intersection)
                if intersection is not None and current_event.key.x <= \
                        intersection.x:
                    event = Event(Type.INTERSECTION, [above, current],
                                  intersection)
                    event_queue.add(event)
            if index + 1 < len(sweep_line_status):
                below = sweep_line_status.get(index + 1)
                intersection = get_intersection(below, current)
                # print("ADD BELOW")
                # print(intersection)
                if intersection is not None and current_event.key.x <= \
                        intersection.x:
                    event = Event(Type.INTERSECTION, [current, below],
                                  intersection)
                    event_queue.add(event)
            if above is not None and below is not None:
                intersection = get_intersection(above, below)
                # print("REMOVE ABOVE BELOW")
                # print(intersection)
                if intersection is not None and current_event.key.x <= \
                        intersection.x:
                    event = Event(Type.INTERSECTION, [above, below],
                                  intersection)
                    event_queue.remove(event)
                    # print("REMOVE")
                    # print(event)
        # END EVENT
        elif current_event.type == Type.END:
            # print("END========================================================")
            current = current_event.segments[0]
            index = sweep_line_status.index(current)
            # print(sweep_line_status)
            # print(index)
            if index - 1 >= 0 and index + 1 < len(sweep_line_status):
                above = sweep_line_status.get(index - 1)
                below = sweep_line_status.get(index + 1)
                intersection = get_intersection(above, below)
                # print("ADD ABOVE BELOW")
                # print(intersection)
                if intersection is not None and current_event.key.x <= \
                        intersection.x:
                    event = Event(Type.INTERSECTION, [above, below],
                                  intersection)
                    event_queue.add(event)
            sweep_line_status.remove(current)
            # print(sweep_line_status)
        # INTERSECTION EVENT
        else:
            # print("INTERSECTION===============================================")
            current1, current2 = current_event.segments[0], \
                                 current_event.segments[1]
            # print(current_event.key)
            result.append(current_event.key)
            # print(current1)
            # print(current2)
            index1 = sweep_line_status.index(current1)
            index2 = sweep_line_status.index(current2)
            # print(index1, index2)
            above = None
            below = None
            if index1 - 1 >= 0:
                above = sweep_line_status.get(index1 - 1)
                intersection = get_intersection(above, current1)
                # print("REMOVE ABOVE")
                # print(intersection)
                if intersection is not None and current_event.key.x <= \
                        intersection.x:
                    event = Event(Type.INTERSECTION, [above, current1],
                                  intersection)
                    event_queue.remove(event)
            if index2 + 1 < len(sweep_line_status):
                below = sweep_line_status.get(index2 + 1)
                intersection = get_intersection(below, current2)
                # print("REMOVE BELOW")
                # print(intersection)
                if intersection is not None and current_event.key.x <= \
                        intersection.x:
                    event = Event(Type.INTERSECTION, [current2, below],
                                  intersection)
                    event_queue.remove(event)
            current1.set_key(current_event.key)
            current2.set_key(current_event.key)
            sweep_line_status.swap_adjacents(index1, index2)
            # print(sweep_line_status)
            # index1 = sweep_line_status.index(current2)
            # index2 = sweep_line_status.index(current1)
            # print(index1, index2)
            if above is not None:
                intersection = get_intersection(above, current2)
                # print("ADD ABOVE")
                # print(intersection)
                if intersection is not None and current_event.key.x <= \
                        intersection.x:
                    event = Event(Type.INTERSECTION, [above, current2],
                                  intersection)
                    event_queue.add(event)
            if below is not None:
                intersection = get_intersection(below, current1)
                # print("ADD BELOW")
                # print(intersection)
                if intersection is not None and current_event.key.x <= \
                        intersection.x:
                    event = Event(Type.INTERSECTION, [current1, below],
                                  intersection)
                    event_queue.add(event)
            # print(sweep_line_status)
    return result, event_order


def update(frame, event_order, ax):
    """
    Updates the plot by frame
    :param frame: frame number
    :param event_order: order of events
    :param ax: subplot object
    :return: None
    """
    # Plotting sweep line and current event
    event = event_order[frame]
    if event.type == Type.START:
        ax.scatter([event.key.x], [event.key.y], s=15, c='b')
    elif event.type == Type.END:
        ax.scatter([event.key.x], [event.key.y], s=15, c='k')
    else:
        ax.scatter([event.key.x], [event.key.y], s=25, c='r')
    plt.axvline(x=event.key.x, color='y', linestyle=':', label='Sweep Line')


def plot_output(segments: list, points: set, event_order: list):
    """
    Plot the points and convex hull
    :param points: Intersections
    :param segments: Line Segments
    :return: None
    """
    print("PLOTTING THE LINE SEGMENTS AND INTERSECTIONS...")
    print("Waiting for plot to be closed...")
    fig, ax = plt.subplots(figsize=(11,8))
    ax.set_title("Sweep Line Algorithm")
    count = 0
    # Plotting Lines
    for segment in segments:
        label = ''
        if count < 1:
            label = "Segment"
        ax.plot([segment.start.x, segment.end.x], [segment.start.y,
                                                 segment.end.y], c='g',
                label=label)
        count += 1
    count = 0
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_aspect('equal')
    ax.legend(bbox_to_anchor=(1.0, 1), loc='upper left', fontsize=7)

    # Animating the plane sweep
    def animate(frame):
        update(frame, event_order, ax)
    animate = FuncAnimation(fig, animate, frames=len(event_order), repeat=False)

    plt.tight_layout()
    plt.show()


def main():
    """
    The main function
    :return: None
    """
    # Check for CLI paramters
    if len(sys.argv) < 2:
        print("Please provide an input file")
        print("USAGE: plane_sweep.py <filename.txt>")
        return
    file_name = str(sys.argv[1])
    output_file_name = "output_plane_sweep.txt"
    # file_name = input("Input file name: ")

    # Reading input
    print("\n============================================================")
    print("READING INPUT FILE: " + file_name)
    number_of_segments, segments = read_input(file_name)
    print(number_of_segments)
    # for segment in segments:
    #     print(segment)

    # Sweep Line
    print("\n============================================================")
    result, event_order = plane_sweep(segments)
    print("\nINTERSECTIONS")
    print(len(result))
    if len(result) <= 500:
        for point in result:
            print(point)

    # Writing output to file
    print("\n============================================================")
    write_output(output_file_name, result)

    # Plotting output
    print("\n============================================================")
    plot_output(segments, result, event_order)


if __name__ == '__main__':
    main()  # Calling Main Function
