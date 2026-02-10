<template>
  <h1>PREP4TEST</h1>
  <br>

  <!--регистрация/авторизация-->
  <div v-if="!user.aut">
    <div class="inputbox">
      <input required="required" type="text" v-model="user.name">
      <span>Имя</span>
      <i></i>
    </div>
    <br>
    <div class="inputbox">
      <input required="required" type="password" v-model="user.pass">
      <span>Пароль</span>
      <i></i>
    </div>
    <p class="error">{{ error }}</p>
    <br>
    <button @click="sendData" class="btn">Отправить</button>
  </div>

  <!-- Меню выбора -->
  <div v-if="user.aut && quiz.Ans">
    <button @click="create_quiz" class="btn">создать викторину</button>
    <br><br>
    <button @click="start_quiz" class="btn">пройти викторину</button>
  </div>

  <!-- Создание викторины -->
  <div v-if="quiz.Create_quiz==true && !quiz.Ans">
    <input type="number" min="2" max="10" step="1" value="2" v-model="quiz.slideCount"> количество слайдов
    <br><br>

    <div class="inputbox">
      <input required="required" type="text" v-model="quiz.title">
      <span>название викторины</span>
      <i></i>
    </div>
    <p class="error">{{ error }}</p>
    <br>
    <button @click="quiz_crt" class="btn">начать создание</button>


  </div>

  <!-- Поиск викторины  -->
  <div v-if="quiz.Start_quiz==true && !quiz.Ans">
    <div class="inputbox">
      <input required="required" type="text" v-model="quiz.id">
      <span>введите id викторины</span>
      <i></i>
    </div>
    <p class="error">{{ error }}</p>
    <br>
    <button @click="quiz_check" class="btn">пройти</button>

  </div>

  <!-- создание слайдов -->
  <div v-if="quiz.continue_create==true">
    <h3>Создание слайда {{ quiz.curslide + 1 }} из {{ quiz.slideCount }}</h3>

    <div class="inputbox">
      <input required="required" type="text" v-model="quiz.slide.question">
      <span>вопрос</span>
      <i></i>
    </div>
<br>
    <div class="inputbox">
      <input required="required" type="text" v-model="quiz.slide.cor">
      <span>правильный ответ</span>
      <i></i>
    </div>
<br>
    <div class="inputbox">
      <input required="required" type="text" v-model="quiz.slide.wrng1">
      <span>1 неверный ответ</span>
      <i></i>
    </div>
<br>
    <div class="inputbox">
      <input required="required" type="text" v-model="quiz.slide.wrng2">
      <span>2 неверный ответ</span>
      <i></i>
    </div>
<br>

    <div class="inputbox">
      <input required="required" type="text" v-model="quiz.slide.wrng3">
      <span>3 неверный ответ</span>
      <i></i>
    </div>
<br>
<p class="error">{{ error }}</p>
    <button @click="next_slide" class="btn">
      {{ quiz.curslide < quiz.slideCount - 1 ? 'Следующий слайд' : 'Завершить создание' }}
    </button>

  </div>

  <!-- Прохождение викторины -->
  <div v-if="false">
    <div v-if="curslide = 1">
      a
    </div>
      
    <div v-else-if="curslide = 2">
      b
    </div>

    <div v-else-if="curslide = 3">
      c
    </div>

    <div v-else-if="curslide = 4">
      d
    </div>

    <div v-else-if="curslide = 5">
      e
    </div>

    <div v-else-if="curslide = 6">
      f
    </div>

    <div v-else-if="curslide = 2">
      g
    </div>

    <div v-else-if="curslide = 2">
      h
    </div>

    <div v-else-if="curslide = 2">
      i
    </div>

    <div v-else>
      j
    </div>
  </div>

</template>



<script>
export default{
  data() {
    return{
      // Свойства пользователя
      user: {
        name: '',
        pass: '',
        aut: false
      },
      users: [],
      error: '',
      
      // Свойства викторины
      quiz: {
        title: '',
        id: '',
        Start_quiz: false,
        Create_quiz: false,
        continue_create: false,
        slideCount: 2,
        curslide: 0,
        Ans: true,
        slide: {
          question: '',
          cor: '',
          wrng1: '',
          wrng2: '',
          wrng3: ''
        },
        slides: []
      },
      quizes: [],
      cur_quiz: null
    }
  },
  methods: {
    sendData() {
      if(this.user.name == '') {
        this.error = 'Имя не введено'
        return;
      }
      if(this.user.pass == '') {
        this.error = 'Пароль не введен'
        return;
      }
      
      this.error = ''
      this.user.aut = true

      this.users.push({
        name: this.user.name,
        pass: this.user.pass
      })
    },
    create_quiz() {
      this.quiz.Ans = false
      this.quiz.Create_quiz = true
    },
    start_quiz() {
      this.quiz.Ans = false
      this.quiz.Start_quiz = true
    },
    back_to_menu() {
      this.quiz.Ans = true
      this.quiz.Start_quiz = false
      this.quiz.Create_quiz = false
      this.quiz.continue_create = false
      this.quiz.id = ''
    },
    quiz_crt() {
      if(this.quiz.title == '') {
        this.error = 'Название не введено'
        return;
      }
      this.error = ''
      this.quiz.continue_create = true
      this.quiz.Create_quiz = false
      this.quiz.slides = []
      
      // Генерируем случайный ID для викторины
      const newId = Math.random().toString(36).substr(2, 9)
      
      this.quizes.push({
        title: this.quiz.title,
        id: newId,
        slideCount: this.quiz.slideCount,
        createdBy: this.user.name
      })
      
      
      

    },
     quiz_check() {
      console.log('Введенный ID:', this.quiz.id);
      console.log('Все викторины:', this.quizes);
      if(this.quiz.id == '') {
        this.error = 'ID не введен'
        return;
      }
      
      // Ищем викторину по ID
      const foundQuiz = this.quizes.find(q => q.id === this.quiz.id)
      
      if(foundQuiz) {
        this.error = `Найдена викторина: ${foundQuiz.title}`
        // Здесь будет логика перехода к прохождению викторины
      } else {
        this.error = 'Викторина с таким ID не найдена'
      }
    },
    next_slide() {
      if (!this.quiz.slide.question || !this.quiz.slide.cor || 
          !this.quiz.slide.wrng1 || !this.quiz.slide.wrng2 || !this.quiz.slide.wrng3) {
        this.error = 'Заполните все поля'
        return;
      }
      
      this.error = ''
      
      // Сохраняем текущий слайд
      this.quiz.slides.push({
        question: this.quiz.slide.question,
        cor: this.quiz.slide.cor,
        wrng1: this.quiz.slide.wrng1,
        wrng2: this.quiz.slide.wrng2,
        wrng3: this.quiz.slide.wrng3
      })
      
      // Очищаем поля для следующего слайда
      this.quiz.slide = {
        question: '',
        cor: '',
        wrng1: '',
        wrng2: '',
        wrng3: ''
      }
      
      // Увеличиваем счетчик слайдов
      this.quiz.curslide++
      
      // Если все слайды созданы, завершаем создание викторины
      if (this.quiz.curslide >= this.quiz.slideCount) {
        this.finish_quiz_creation()
      }
    },
    finish_quiz_creation() {
      // Сохраняем викторину в общий список
      this.quizes.push({
        title: this.quiz.title,
        id: this.currentQuizId,
        slideCount: this.quiz.slideCount,
        slides: [...this.quiz.slides], // Копируем массив слайдов
        createdBy: this.user.name
      
      })
      this.back_to_menu()
    }
  
  }
}
</script>


<style scoped>

/*кнопка*/
/* From Uiverse.io by nikk7007 */ 
.btn {
 --color: #00A97F;
 --color2: rgb(10, 25, 30);
 padding: 0.8em 1.75em;
 background-color: transparent;
 border-radius: 6px;
 border: .3px solid var(--color);
 transition: .5s;
 position: relative;
 overflow: hidden;
 cursor: pointer;
 z-index: 1;
 font-weight: 300;
 font-size: 17px;
 font-family: 'Roboto', 'Segoe UI', sans-serif;
 text-transform: uppercase;
 color: var(--color);
}

.btn::after, .btn::before {
 content: '';
 display: block;
 height: 100%;
 width: 100%;
 transform: skew(90deg) translate(-50%, -50%);
 position: absolute;
 inset: 50%;
 left: 25%;
 z-index: -1;
 transition: .5s ease-out;
 background-color: var(--color);
}

.btn::before {
 top: -50%;
 left: -25%;
 transform: skew(90deg) rotate(180deg) translate(-50%, -50%);
}

.btn:hover::before {
 transform: skew(45deg) rotate(180deg) translate(-50%, -50%);
}

.btn:hover::after {
 transform: skew(45deg) translate(-50%, -50%);
}

.btn:hover {
 color: var(--color2);
}

.btn:active {
 filter: brightness(.7);
 transform: scale(.98);
}



/* From Uiverse.io by VijinV */ 
/*ввод текста*/
.inputbox {
  position: relative;
  width: 196px;
}

.inputbox input {
  position: relative;
  width: 100%;
  padding: 20px 10px 10px;
  background: transparent;
  outline: none;
  box-shadow: none;
  border: none;
  color: #23242a;
  font-size: 1em;
  letter-spacing: 0.05em;
  transition: 0.5s;
  z-index: 10;
}

.inputbox span {
  position: absolute;
  left: 0;
  padding: 20px 10px 10px;
  font-size: 1em;
  color: #8f8f8f;
  letter-spacing: 00.05em;
  transition: 0.5s;
  pointer-events: none;
}

.inputbox input:valid ~span,
.inputbox input:focus ~span {
  color: #45f3ff;
  transform: translateX(-10px) translateY(-34px);
  font-size: 0,75em;
}

.inputbox i {
  position: absolute;
  left: 0;
  bottom: 0;
  width: 100%;
  height: 2px;
  background: #45f3ff;
  border-radius: 4px;
  transition: 0.5s;
  pointer-events: none;
  z-index: 9;
}

.inputbox input:valid ~i,
.inputbox input:focus ~i {
  height: 44px;
}
</style>
