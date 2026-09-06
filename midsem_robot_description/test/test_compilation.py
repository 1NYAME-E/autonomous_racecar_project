# Making the necessary imports
import os
import subprocess
import unittest

from ament_index_python.packages import get_package_share_directory


class TestURDFCompilation(unittest.TestCase):
    def test_xacro_build(self):
        """
        Tests if the main robot.urdf.xacro file compiles successfully 
        without any XML or Xacro macro syntax errors.
        """
        # Locating the package directory
        try:
            pkg_share = get_package_share_directory('midsem_robot_description')
        except Exception as e:
            self.fail(
                f"Could not find package share directory. Error: {e}")

        # Path to the main xacro file
        xacro_file = os.path.join(pkg_share, 'urdf', 'robot.urdf.xacro')

        # Ensuring that the file actually exists
        self.assertTrue(os.path.exists(xacro_file),
                        f"Xacro file not found at: {xacro_file}")

        # Running the xacro command
        result = subprocess.run(['xacro', xacro_file],
                                capture_output=True, text=True)

        # Assert that the command completed without any errors 
        self.assertEqual(
            result.returncode,
            0,
            f"Xacro compilation failed\nError Output:\n{result.stderr}"
        )


if __name__ == '__main__':
    unittest.main()
