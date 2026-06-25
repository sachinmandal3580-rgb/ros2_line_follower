#!/usr/bin/env python3
"""
ROBOTRACE - Follower Node (STUDENT TODO VERSION)
==================================================
This is the "brain" of the robot. It reads camera frames, detects the
track line using OpenCV, computes how far the robot has drifted from
the center of the line, and publishes velocity commands to correct
that drift.

Several core pieces of logic have been removed and replaced with
TODO blocks. Read each TODO carefully - it tells you exactly what
the missing code needs to do, what variables/values it should use,
and what the rest of the node expects from it.

Do NOT change function signatures, global variable names, or the
overall node structure - only fill in the TODO sections.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty

import numpy as np
import cv2
import cv_bridge

bridge = cv_bridge.CvBridge()

# -----------------------------------------------------------------------
# TUNING PARAMETERS
# -----------------------------------------------------------------------
MIN_AREA = 500            # Minimum contour area to be considered "noise filtered"
MIN_AREA_TRACK = 5000     # Minimum contour area to be considered the main track line
LINEAR_SPEED = 0.2        # Constant forward speed while line is visible
KP = 1.5 / 100            # Proportional gain for the steering controller
LOSS_FACTOR = 1.2         # Amplification factor applied to the last known error when line is lost
TIMER_PERIOD = 0.06       # Seconds between each control loop tick
FINALIZATION_PERIOD = 4   # Seconds to count down once the finish condition is detected
MAX_ERROR = 30            # Max allowed error to count a marker detection as "centered enough"

# Color threshold range (BGR) used to mask out the track line from the rest of the image
lower_bgr_values = np.array([31, 42, 53])
upper_bgr_values = np.array([255, 255, 255])


def crop_size(height, width):
    """
    TODO 1: Define the Region of Interest (ROI)
    ---------------------------------------------
    Return a tuple: (crop_h_start, crop_h_stop, crop_w_start, crop_w_stop)

    Goal: We only want to look at a horizontal strip near the BOTTOM of the
    image (since that's where the track line will be closest to the robot),
    and only the MIDDLE portion of the image width (to ignore clutter on
    the far left/right edges of the frame).

    Think about it in terms of fractions of `height` and `width`. For example:
      - Vertically: skip the top portion of the image, keep everything below it.
      - Horizontally: keep a centered band, ignoring the outer edges.

    Return integers, since these will be used as array slice indices.
    """
    # Replace this line with your own calculation:
    raise NotImplementedError("TODO 1: implement crop_size()")


# -----------------------------------------------------------------------
# GLOBAL STATE
# -----------------------------------------------------------------------
image_input = 0
error = 0
just_seen_line = False
just_seen_right_mark = False
should_move = False
right_mark_count = 0
finalization_countdown = None


def start_follower_callback(request, response):
    global should_move, right_mark_count, finalization_countdown
    should_move = True
    right_mark_count = 0
    finalization_countdown = None
    return response


def stop_follower_callback(request, response):
    global should_move, finalization_countdown
    should_move = False
    finalization_countdown = None
    return response


def image_callback(msg):
    """Stores the latest camera frame as an OpenCV (numpy) image."""
    global image_input
    image_input = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')


def get_contour_data(mask, out):
    """
    TODO 2: Extract the track line and marker positions from contours
    --------------------------------------------------------------------
    `mask` is a binary (black/white) image where the track line (and any
    markers) appear as white blobs. `out` is the image to draw debug
    visuals onto (for your own sanity-checking - drawing is optional but
    recommended).

    You need to:
      1. Find all contours in `mask` using cv2.findContours()
         (use cv2.RETR_EXTERNAL and cv2.CHAIN_APPROX_NONE).
      2. For each contour, compute its moments with cv2.moments().
      3. Use M['m00'] as the contour's AREA to decide what it is:
           - If area > MIN_AREA_TRACK  -> this is the MAIN TRACK LINE.
                Store its centroid in a dict called `line` with keys
                'x' and 'y'. NOTE: 'x' must be offset by `crop_w_start`
                (the global set in timer_callback) so it maps back to
                full-image coordinates.
           - elif area > MIN_AREA      -> this is a possible MARKER.
                Store its centroid in a dict called `mark` with keys
                'x' and 'y' (also offset 'x' by crop_w_start).
                If there are multiple marker-sized contours, keep only
                the one with the SMALLEST 'y' (i.e. the topmost one).
           - otherwise -> ignore it (too small / noise).
      4. Determine `mark_side`:
           - If both `mark` and `line` were found, compare mark['x']
             vs line['x']: if mark is to the right of the line, set
             mark_side = "right", otherwise "left".
           - If no marker was found, mark_side = None.
      5. Return a tuple: (line, mark_side)

    Centroid formula reminder:
        cx = M['m10'] / M['m00']
        cy = M['m01'] / M['m00']
    """
    raise NotImplementedError("TODO 2: implement get_contour_data()")


def timer_callback():
    """
    Main control loop - runs every TIMER_PERIOD seconds.
    """
    global error, image_input, just_seen_line, just_seen_right_mark
    global should_move, right_mark_count, finalization_countdown

    if type(image_input) != np.ndarray:
        return

    height, width, _ = image_input.shape
    image = image_input.copy()

    global crop_w_start
    crop_h_start, crop_h_stop, crop_w_start, crop_w_stop = crop_size(height, width)

    crop = image[crop_h_start:crop_h_stop, crop_w_start:crop_w_stop]

    # ---------------------------------------------------------------
    # TODO 3: Build the binary mask of the track line
    # ---------------------------------------------------------------
    # Use cv2.inRange() with `lower_bgr_values` and `upper_bgr_values`
    # on `crop` to produce a binary mask highlighting the track color.
    # Store the result in a variable named `mask`.
    mask = None  # <-- replace this
    raise NotImplementedError("TODO 3: build the color mask")

    output = image
    line, mark_side = get_contour_data(mask, output[crop_h_start:crop_h_stop, crop_w_start:crop_w_stop])

    message = Twist()

    # ---------------------------------------------------------------
    # TODO 4: Compute the steering error and handle line loss
    # ---------------------------------------------------------------
    # If `line` was found (i.e. the dict is non-empty):
    #   - Compute `error` = (x position of the line) - (center of the image, width//2)
    #   - Set message.linear.x = LINEAR_SPEED
    #   - Set just_seen_line = True
    #   - (optional) draw a circle on `output` at the line's position for debugging
    #
    # Else (line not found / lost):
    #   - If we had JUST seen the line a moment ago (just_seen_line is True):
    #       - Set just_seen_line = False
    #       - Amplify the last known `error` by multiplying it with LOSS_FACTOR
    #         (this makes the robot turn harder to try to re-find the line)
    #   - Set message.linear.x = 0.0 (don't drive blindly forward while searching)
    raise NotImplementedError("TODO 4: compute error and handle recovery behavior")

    # ---------------------------------------------------------------
    # TODO 5: Marker / lap-completion detection
    # ---------------------------------------------------------------
    # If `mark_side` is not None (a marker was detected):
    #   - Print the mark_side for debugging
    #   - If ALL of the following are true:
    #       * mark_side == "right"
    #       * finalization_countdown is None (we haven't already started finishing)
    #       * abs(error) <= MAX_ERROR  (robot is reasonably centered when it sees the marker)
    #       * just_seen_right_mark is False (this is a NEW marker sighting, not the same one repeated)
    #     Then:
    #       - Increment right_mark_count
    #       - If right_mark_count > 1 (this is the SECOND right-side marker seen,
    #         i.e. one full lap completed):
    #           - Set finalization_countdown = int(FINALIZATION_PERIOD / TIMER_PERIOD) + 1
    #           - Print a message announcing finalization has begun
    #   - Set just_seen_right_mark = True
    # Else (no marker detected this frame):
    #   - Set just_seen_right_mark = False
    raise NotImplementedError("TODO 5: implement marker / lap counting logic")

    # ---------------------------------------------------------------
    # TODO 6: Proportional control law
    # ---------------------------------------------------------------
    # Set message.angular.z using proportional control:
    #     angular.z = error * -KP
    # Print the error and angular.z for debugging.
    raise NotImplementedError("TODO 6: implement the proportional control law")

    cv2.rectangle(output, (crop_w_start, crop_h_start), (crop_w_stop, crop_h_stop), (0, 0, 255), 2)
    cv2.imshow("output", output)
    cv2.waitKey(5)

    # ---------------------------------------------------------------
    # TODO 7: Finalization countdown and safe shutdown
    # ---------------------------------------------------------------
    # If finalization_countdown is not None:
    #   - If it's greater than 0: decrement it by 1
    #   - If it's exactly 0:
    #       - Set should_move = False
    #       - Publish an empty Twist() to stop the robot
    #       - Print "Track Completed"
    #       - Destroy all OpenCV windows
    #       - Destroy the node and call rclpy.shutdown()
    #       - return (so we don't fall through to publishing more commands)
    raise NotImplementedError("TODO 7: implement the finalization/shutdown sequence")

    if should_move:
        publisher.publish(message)
    else:
        empty_message = Twist()
        publisher.publish(empty_message)


def main():
    rclpy.init()
    global node
    node = Node('follower')

    # -------------------------------------------------------------------
    # TODO 8: Wire up the node's publisher, subscriber, timer, and services
    # -------------------------------------------------------------------
    # You need to create:
    #   1. `publisher` (global) - a publisher on the '/cmd_vel' topic,
    #      message type Twist, using rclpy.qos.qos_profile_system_default.
    #   2. A subscription to the 'camera/image_raw' topic, message type
    #      Image, callback = image_callback, using
    #      rclpy.qos.qos_profile_sensor_data.
    #   3. A timer that calls `timer_callback` every TIMER_PERIOD seconds.
    #   4. Two services:
    #       - 'start_follower' (type Empty) -> start_follower_callback
    #       - 'stop_follower'  (type Empty) -> stop_follower_callback
    #
    # Hint: look at how `node.create_publisher`, `node.create_subscription`,
    # `node.create_timer`, and `node.create_service` are used elsewhere
    # in this project (e.g. the camera test script) for the exact syntax.
    raise NotImplementedError("TODO 8: set up publisher, subscriber, timer, and services")

    rclpy.spin(node)


try:
    main()
except (KeyboardInterrupt, rclpy.exceptions.ROSInterruptException):
    empty_message = Twist()
    publisher.publish(empty_message)
    node.destroy_node()
    rclpy.shutdown()
    exit()