import os
import subprocess
from lexer import lex
from parser import Parser

class MoonInterpreter:
    def __init__(self, base_dir="."):
        # Define directories relative to your GitHub layout
        self.modules_dir = os.path.join(base_dir, "Modules")
        self.package_dir = os.path.join(base_dir, "Package")
        
        # This keeps track of variables declared via 'vocal'
        self.variables = {}

    def interpret(self, ast):
        """Loops through every node in the AST and executes it."""
        for node in ast:
            self.execute_node(node)

    def execute_node(self, node):
        node_type = node.get("type")

        # 1. Handle: download ModuleName
        if node_type == "DownloadStatement":
            module_name = node["module_name"]
            
            # ROUTING RULE: If it matches your documented JS packages, route to /Package
            if module_name in ["3dSite", "MathExtreme", "DrawingIO"]:
                self.load_js_package(module_name)
            else:
                self.load_native_module(module_name)

        # 2. Handle: vocal VariableName
        elif node_type == "VocalStatement":
            var_name = node["variable_name"]
            # Initialize the variable in memory (defaults to empty string or null)
            self.variables[var_name] = "Hello from Moon Script variable!" 
            print(f"[Moon VM] Registered variable: {var_name}")

        # 3. Handle: break(...)
        elif node_type == "BreakStatement":
            arg = node["argument"]
            
            if arg["type"] == "StringLiteral":
                print(arg["value"])
                
            elif arg["type"] == "VariableReference":
                var_name = arg["value"]
                if var_name in self.variables:
                    print(self.variables[var_name])
                else:
                    print(f"Moon Runtime Error: Variable '{var_name}' is not defined.")

    def load_native_module(self, name):
        """Loads and executes a native .mn module from /Modules."""
        path = os.path.join(self.modules_dir, f"{name}.mn")
        if not os.path.exists(path):
            print(f"Moon Linker Error: Native module '{name}' not found at {path}")
            return
            
        print(f"[Moon Linker] Executing native module: {name}")
        with open(path, "r") as f:
            module_code = f.read()
            
        # Recursive execution: Lex, parse, and interpret the native module
        tokens = lex(module_code)
        parser = Parser(tokens)
        module_ast = parser.parse()
        self.interpret(module_ast)

    def load_js_package(self, name):
        """Spins up Node.js to handle JavaScript packages from /Package."""
        path = os.path.join(self.package_dir, f"{name}.js")
        if not os.path.exists(path):
            print(f"Moon Linker Error: JS Package '{name}' not found at {path}")
            return

        print(f"[Moon Linker] Launching JavaScript package: {name}")
        try:
            # Execute the JS package using Node.js background processes
            result = subprocess.run(["node", path], capture_output=True, text=True, check=True)
            if result.stdout:
                print(f"[JS Package Output]:\n{result.stdout.strip()}")
        except subprocess.CalledProcessError as e:
            print(f"Moon Runtime Error inside JS Package:\n{e.stderr}")
