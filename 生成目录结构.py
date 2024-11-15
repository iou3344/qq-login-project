import os

def create_project_structure():
    # 项目结构定义
    structure = {
        'project': {
            'main.py': '',
            'db': {
                '__init__.py': '',
                'db_handler.py': '',
                'secondary_db.py': ''
            },
            'ui': {
                '__init__.py': '',
                'main_window.py': '',
                'data_panel.py': '',
                'panels': {
                    '__init__.py': '',
                    'file_panel.py': '',
                    'query_panel.py': '',
                    'value_match_panel.py': '',
                    'combined_query_panel.py': '',
                    'login_panel.py': ''
                }
            },
            'core': {
                '__init__.py': '',
                'data_loader.py': '',
                'query_manager.py': '',
                'value_matcher.py': '',
                'combined_matcher.py': '',
                'login_manager.py': ''
            },
            'utils': {
                '__init__.py': '',
                'signals.py': '',
                'config.py': ''
            }
        }
    }

    def create_files(base_path, structure):
        for name, content in structure.items():
            path = os.path.join(base_path, name)
            if isinstance(content, dict):
                os.makedirs(path, exist_ok=True)
                create_files(path, content)
            else:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write('')
                print(f'Created file: {path}')

    # 创建项目根目录
    project_path = os.path.join(os.getcwd(), 'project')
    if not os.path.exists(project_path):
        os.makedirs(project_path)
        print(f'Created directory: {project_path}')

    # 创建文件结构
    create_files(os.getcwd(), structure)

if __name__ == '__main__':
    create_project_structure()