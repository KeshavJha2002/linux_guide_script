info_format_ = """
        json{
        "mkdir": [{
            "syntax": "mkdir [options] directory_name...",
            "description": "Creates one or more directories (folders). If the directory already exists, an error message will be printed.",
            "options": {
                "-p": "Creates any necessary parent directories.",
                "-v": "Prints the name of each directory created.",
                "-m mode": "Sets the permissions of the new directory to the specified mode.",
                "-Z context": "Sets the SELinux security context of the new directory to the specified value."
            },
            "examples": [
                {
                    "command": "mkdir mydir",
                    "explanation": "Creates a directory named 'mydir'."
                },
                {
                    "command": "mkdir -p mydir/sub1/sub2",
                    "explanation": "Creates a directory named 'mydir' and any necessary parent directories."
                },
                {
                    "command": "mkdir -m 755 mydir",
                    "explanation": "Creates a directory named 'mydir' with permissions set to 755."
                },
                {
                    "command": "mkdir -Z context=user_home_t mydir",
                    "explanation": "Creates a directory named 'mydir' with the specified SELinux security context."
                }
            ]
        }
        ]
        }
        """

scenario_format_ = """
        json{
        "scenario": "I want to change the file write access to the admin only.",
        "commands": [
            {
                "description": "Using symbolic permissions",
                "command": "sudo chmod u=rw,go= /path/to/your/file"
            },
            {
                "description": "Using octal notation",
                "command": "sudo chmod 600 /path/to/your/file"
            },
            {
                "description": "Using symbolic permissions with shorthand",
                "command": "sudo chmod u+w /path/to/your/file && sudo chmod go= /path/to/your/file"
            },
            {
                "description": "Using symbolic permissions with absolute specification",
                "command": "sudo chmod u=rw,g=,o= /path/to/your/file"
            }
        ]
        }
        """