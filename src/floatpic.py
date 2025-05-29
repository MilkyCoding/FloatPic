import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from typing import Optional

class FloatPicApp:
    """Приложение для отображения изображений поверх всех окон."""
    
    def __init__(self):
        # Настройка темы
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Создание основного окна
        self.root = ctk.CTk()
        self.root.title("FloatPic")
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 1.0)
        
        # Состояние приложения
        self.current_image: Optional[ImageTk.PhotoImage] = None
        self.original_image: Optional[Image.Image] = None
        self.image_path: Optional[str] = None
        self.is_hidden: bool = False
        
        self._setup_ui()
        self._bind_events()

    def _setup_ui(self) -> None:
        """Настройка пользовательского интерфейса."""
        # Основной контейнер
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True)
        
        # Область для изображения
        self.image_label = ctk.CTkLabel(self.main_frame, text="")
        self.image_label.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Панель управления
        self.control_frame = ctk.CTkFrame(self.main_frame)
        self.control_frame.pack(fill="x", padx=5, pady=5)
        
        # Кнопки управления
        self.open_button = ctk.CTkButton(
            self.control_frame,
            text="Открыть",
            command=self._open_image,
            width=100
        )
        self.open_button.pack(side="left", padx=5)
        
        self.toggle_button = ctk.CTkButton(
            self.control_frame,
            text="Скрыть",
            command=self._toggle_visibility,
            width=100
        )
        self.toggle_button.pack(side="left", padx=5)
        
        self.close_button = ctk.CTkButton(
            self.control_frame,
            text="Закрыть",
            command=self._quit_app,
            width=100,
            fg_color="#E74C3C",
            hover_color="#C0392B"
        )
        self.close_button.pack(side="left", padx=5)
        
        # Ползунок прозрачности
        self.opacity_label = ctk.CTkLabel(self.control_frame, text="Прозрачность:")
        self.opacity_label.pack(side="left", padx=(10, 0))
        
        self.opacity_scale = ctk.CTkSlider(
            self.control_frame,
            from_=0.1,
            to=1.0,
            number_of_steps=90,
            command=self._update_opacity
        )
        self.opacity_scale.set(1.0)
        self.opacity_scale.pack(side="left", padx=5, fill="x", expand=True)

    def _bind_events(self) -> None:
        """Привязка горячих клавиш."""
        self.root.bind('<Control-h>', lambda e: self._toggle_visibility())
        self.root.bind('<Control-q>', lambda e: self._quit_app())

    def _open_image(self) -> None:
        """Открытие диалога выбора изображения."""
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Изображения", "*.png *.jpg *.jpeg *.gif"),
                ("Все файлы", "*.*")
            ]
        )
        
        if file_path:
            try:
                self._load_image(file_path)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {str(e)}")

    def _load_image(self, file_path: str) -> None:
        """Загрузка и отображение изображения."""
        self.original_image = Image.open(file_path)
        
        # Масштабируем изображение, если оно слишком большое
        max_size = (800, 600)
        if self.original_image.size[0] > max_size[0] or self.original_image.size[1] > max_size[1]:
            self.original_image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        self._update_image_display()
        self.image_path = file_path
        
        # Обновляем размер окна под изображение
        window_width = self.original_image.size[0] + 10
        window_height = self.original_image.size[1] + 60
        self.root.geometry(f"{window_width}x{window_height}")

    def _update_image_display(self) -> None:
        """Обновление отображения изображения."""
        if self.original_image:
            self.current_image = ImageTk.PhotoImage(self.original_image)
            self.image_label.configure(image=self.current_image)

    def _update_opacity(self, value: float) -> None:
        """Обновление прозрачности окна."""
        self.root.attributes('-alpha', float(value))

    def _toggle_visibility(self) -> None:
        """Переключение видимости окна."""
        self.is_hidden = not self.is_hidden
        if self.is_hidden:
            self.root.withdraw()
            self.toggle_button.configure(text="Показать")
        else:
            self.root.deiconify()
            self.toggle_button.configure(text="Скрыть")

    def _quit_app(self) -> None:
        """Завершение работы приложения."""
        self.root.quit()

    def run(self) -> None:
        """Запуск приложения."""
        self.root.mainloop()

if __name__ == "__main__":
    app = FloatPicApp()
    app.run() 