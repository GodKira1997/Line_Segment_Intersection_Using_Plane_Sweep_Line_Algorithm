"""
file: brute_force.py
description: This program performs a brute force algorithm to solve the line
segment intersection problem and visualize it.
language: python3
author: Anurag Kallurwar, ak6491@rit.edu
"""

import sys
from enum import Enum
# Install matplotlib using pip
import matplotlib.pyplot as plt


class Point():
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


def brute_force(segments: list):
    """
    This method implements a brute force algorithm to find intersections
    :param segments: The input line segments (list of Segment objects)
    :return: Intersection Point Objects
    """
    print("\nSTARTING BRUTE FORCE...")
    result = []
    for index1 in range(len(segments)):
        for index2 in range(index1, len(segments)):
            intersection = get_intersection(segments[index1], segments[index2])
            if intersection is not None:
                result.append(intersection)
    return result


def plot_output(segments: list, points: set):
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
    for segment in segments:
        label = ''
        if count < 1:
            label = "Segment"
        ax.plot([segment.start.x, segment.end.x], [segment.start.y,
                                                 segment.end.y], c='y',
                label=label)
        if count < 1:
            label = "Start Point"
        ax.scatter([segment.start.x], [segment.start.y], s=10, c='b',
                   label=label)
        if count < 1:
            label = "End Point"
        ax.scatter([segment.end.x], [segment.end.y], s=10, c='r', label=label)
        count += 1
    count = 0
    for point in list(points):
        label = ''
        if count < 1:
            label = "Intersection Point"
        ax.scatter([point.x], [point.y], s=20, c='g', label=label)
        count += 1
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_aspect('equal')
    ax.legend(bbox_to_anchor=(1.0, 1), loc='upper left', fontsize=7)
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
    output_file_name = "output_brute_force.txt"
    # file_name = input("Input file name: ")

    # Reading input
    print("\n============================================================")
    print("READING INPUT FILE: " + file_name)
    number_of_segments, segments = read_input(file_name)
    print(number_of_segments)
    # for segment in segments:
    #     print(segment)

    # Brute Force
    print("\n============================================================")
    result = brute_force(segments)
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
    plot_output(segments, result)


if __name__ == '__main__':
    main()  # Calling Main Function
