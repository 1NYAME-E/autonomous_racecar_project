# Making the necessary imports
import os
import subprocess
import unittest
import xml.etree.ElementTree as ET

from ament_index_python.packages import get_package_share_directory


class TestURDFStructure(unittest.TestCase):
    def setUp(self):
        """Compiles the Xacro file into an XML string before running tests."""
        pkg_share = get_package_share_directory('midsem_robot_description')
        xacro_file = os.path.join(pkg_share, 'urdf', 'robot.urdf.xacro')

        # Compiling the .xacro file
        result = subprocess.run(['xacro', xacro_file],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0,
                         "Failed to compile Xacro in setup.")
        self.urdf_root = ET.fromstring(result.stdout)

    def test_sensor_links_exist(self):
        """Verifies that the LiDAR and Camera links are successfully generated."""
        # Find all the <link> tags and extracting their names
        links = [link.get('name') for link in self.urdf_root.findall('link')]

        # Asserting that all the sensors exist
        self.assertIn('laser_frame', links,
                      "CRITICAL: LiDAR 'laser_frame' is missing from the compiled URDF!")
        self.assertIn('camera_link', links,
                      "CRITICAL: Camera 'camera_link' is missing from the compiled URDF!")

    def test_wheel_links_exist(self):
        """Verifying that all four wheels for the Ackermann drive are present."""
        links = [link.get('name') for link in self.urdf_root.findall('link')]

        self.assertIn('front_left_wheel', links)
        self.assertIn('front_right_wheel', links)
        self.assertIn('rear_left_wheel', links)
        self.assertIn('rear_right_wheel', links)


if __name__ == '__main__':
    unittest.main()
