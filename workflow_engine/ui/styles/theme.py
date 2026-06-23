"""主题管理"""
import os
from pathlib import Path
from typing import Dict, Optional
from PySide6.QtCore import QSettings


class Theme:
    """主题配置"""
    
    THEMES = {
        'light': {
            'name': '浅色',
            'base': 'base.qss',
            'components': 'components.qss',
            'colors': {
                'primary': '#2196F3',
                'secondary': '#64B5F6',
                'accent': '#FF9800',
                'background': '#FAFAFA',
                'surface': '#FFFFFF',
                'text': '#212121',
                'text_secondary': '#757575',
                'border': '#E0E0E0',
                'error': '#F44336',
                'success': '#4CAF50',
                'warning': '#FFC107',
            }
        },
        'dark': {
            'name': '深色',
            'base': 'base.qss',
            'components': 'components.qss',
            'colors': {
                'primary': '#2196F3',
                'secondary': '#64B5F6',
                'accent': '#FF9800',
                'background': '#121212',
                'surface': '#1E1E1E',
                'text': '#FFFFFF',
                'text_secondary': '#B0B0B0',
                'border': '#424242',
                'error': '#CF6679',
                'success': '#81C784',
                'warning': '#FFD54F',
            }
        },
        'blue': {
            'name': '蓝色',
            'base': 'base.qss',
            'components': 'components.qss',
            'colors': {
                'primary': '#1976D2',
                'secondary': '#42A5F5',
                'accent': '#00BCD4',
                'background': '#E3F2FD',
                'surface': '#FFFFFF',
                'text': '#0D47A1',
                'text_secondary': '#1565C0',
                'border': '#BBDEFB',
                'error': '#D32F2F',
                'success': '#388E3C',
                'warning': '#F57C00',
            }
        },
    }
    
    _current_theme: str = 'light'
    _colors: Dict[str, str] = THEMES['light']['colors']
    
    @classmethod
    def get_stylesheet(cls) -> str:
        """获取完整的样式表"""
        theme = cls.THEMES.get(cls._current_theme, cls.THEMES['light'])
        styles_dir = Path(__file__).parent
        
        qss_files = [
            'base.qss',
            'components.qss',
            'canvas.qss',
            'node_panel.qss',
            'property_panel.qss',
            'log_panel.qss',
            'toolbar.qss',
            'menu.qss',
        ]
        
        stylesheet = ''
        for qss_file in qss_files:
            qss_path = styles_dir / qss_file
            if qss_path.exists():
                with open(qss_path, 'r', encoding='utf-8') as f:
                    stylesheet += f.read() + '\n'
        
        for key in sorted(cls._colors.keys(), key=len, reverse=True):
            stylesheet = stylesheet.replace(f'@{key}', cls._colors[key])
        
        return stylesheet
    
    @classmethod
    def set_theme(cls, theme_name: str):
        """设置主题"""
        if theme_name in cls.THEMES:
            cls._current_theme = theme_name
            cls._colors = cls.THEMES[theme_name]['colors']
    
    @classmethod
    def get_current_theme(cls) -> str:
        """获取当前主题名称"""
        return cls._current_theme
    
    @classmethod
    def get_colors(cls) -> Dict[str, str]:
        """获取当前主题颜色"""
        return cls._colors.copy()


_theme_instance = Theme()


def get_theme() -> Theme:
    """获取主题实例"""
    return _theme_instance


def set_theme(theme_name: str):
    """设置全局主题"""
    Theme.set_theme(theme_name)
