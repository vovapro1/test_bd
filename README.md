Проект по sqlalchemy симулирующий работу с таблицей резюме зверей мечтающих попасть в ит.

Основной класс для работы с sqlalchemy написан в файле src/queries/orm
Методы класса Work_Table_ORM позволяют создавать/редактировать/выполнять поиск по ранее созданным таблицам, с помощью орм.

На сегодняшний день (26.07.2024) ведется работа по настройки работы в файле Jupiter NoteBook для конвертации возвращаемых данных от orm DTO обьектам (data transfr object), с последующей работой в FastAPI