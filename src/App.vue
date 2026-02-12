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
    <br>
    <br>
    <button @click="back_to_menu" class="btn">отмена</button>


  </div>

  <!-- Поиск викторины  -->
  <div v-if="quiz.Start_quiz==true && !quiz.Ans && !quiz.isPlaying">
    <div class="inputbox">
      <input required="required" type="text" v-model="quiz.title">
      <span>название викторины</span>
      <i></i>
    </div>
    <p class="error">{{ error }}</p>
    <br>
    <button @click="quiz_check" class="btn">пройти</button>
    <br>
    <br>
    <button @click="back_to_menu" class="btn">отмена</button>

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

<!--прохождение викторины -->
  <div v-if="quiz.isPlaying">
    <h2>Викторина: {{ currentQuiz.title }}</h2>
    <h3>Вопрос {{ quiz.currentSlideIndex + 1 }} из {{ currentQuiz.slideCount }}</h3>
    
    <div class="question-container">
      <h3>{{ currentSlide.question }}</h3>
      
      <div v-for="(option, index) in shuffledOptions" :key="index" class="quantum-radio" @click="selectOption(option)">
        <input 
          type="radio" 
          :id="'option' + index" 
          :value="option" 
          v-model="selectedOption"
          :name="'question' + quiz.currentSlideIndex"
        >
        <label :for="'option' + index" class="radio-control"></label>
        <span class="radio-label">{{ option }}</span>
      </div>
      
      <button @click="nextQuestion" class="btn" :disabled="!selectedOption">
        {{ quiz.currentSlideIndex < currentQuiz.slideCount - 1 ? 'Следующий вопрос' : 'Завершить' }}
      </button>
      
      <div v-if="showResult" class="result">
        <p :class="{ correct: isCorrect, incorrect: !isCorrect }">
          {{ isCorrect ? 'Правильно!' : 'Неправильно!' }}
        </p>
        <p v-if="!isCorrect && showCorrectAnswer">
          Правильный ответ: {{ currentSlide.cor }}
        </p>
      </div>
    </div>
    
    <br>
    <button @click="exitQuiz" class="btn">Выйти из викторины</button>
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
        Start_quiz: false,
        Create_quiz: false,
        continue_create: false,
        slideCount: 2,
        curslide: 0,
        Ans: true,
        isPlaying: false,
        currentSlideIndex: 0,
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
      currentQuiz: null, // ИСПРАВЛЕНО: было cur_quiz: null
      selectedOption: '',
      showResult: false,
      isCorrect: false,
      showCorrectAnswer: false,
      shuffledOptions: []
    }
  },
  computed: {  // ПЕРЕМЕЩЕНО: computed должен быть перед methods
    currentSlide() {
      if (this.currentQuiz && this.currentQuiz.slides) {
        return this.currentQuiz.slides[this.quiz.currentSlideIndex];
      }
      return null;
    }
  },
  watch: {  // watch после computed
    'quiz.currentSlideIndex': {
      handler() {
        this.shuffleOptions();
        this.resetQuestionState();
      },
      immediate: false
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
      this.quiz.isPlaying = false
      this.currentQuiz = null
      this.error = ''
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
      this.quiz.curslide = 0 // ДОБАВЛЕНО
    },
    quiz_check() {
      console.log('Все викторины:', this.quizes);
      if(this.quiz.title == '') {
        this.error = 'Название не введено' // ИСПРАВЛЕНО
        return;
      }
      
      // Ищем викторину по названию
      const foundQuiz = this.quizes.find(q => q.title === this.quiz.title) // ИСПРАВЛЕНО
      
      if(foundQuiz) { // ИСПРАВЛЕНО
        this.error = ''
        this.currentQuiz = foundQuiz
        this.quiz.isPlaying = true
        this.quiz.Start_quiz = false
        this.quiz.currentSlideIndex = 0
        this.$nextTick(() => { // ДОБАВЛЕНО: ждем обновления DOM
          this.shuffleOptions()
          this.resetQuestionState()
        })
      } else {
        this.error = 'Викторина с таким названием не найдена'
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
        slideCount: this.quiz.slideCount,
        slides: [...this.quiz.slides],
        createdBy: this.user.name
      })
      this.back_to_menu()
    },
    shuffleOptions() {
      if (this.currentSlide) {
        const options = [
          this.currentSlide.cor,
          this.currentSlide.wrng1,
          this.currentSlide.wrng2,
          this.currentSlide.wrng3
        ];
        
        // Перемешиваем массив опций
        for (let i = options.length - 1; i > 0; i--) {
          const j = Math.floor(Math.random() * (i + 1));
          [options[i], options[j]] = [options[j], options[i]];
        }
        
        this.shuffledOptions = options;
      }
    },
    selectOption(option) {
      this.selectedOption = option;
    },
    nextQuestion() {
      if (!this.currentSlide) return;
      
      // Проверяем правильность ответа
      this.isCorrect = this.selectedOption === this.currentSlide.cor;
      this.showResult = true;
      this.showCorrectAnswer = !this.isCorrect;
      
      setTimeout(() => {
        if (this.quiz.currentSlideIndex < this.currentQuiz.slideCount - 1) {
          // Переходим к следующему вопросу
          this.quiz.currentSlideIndex++;
        } else {
          // Завершаем викторину
          this.exitQuiz();
        }
        this.resetQuestionState();
      }, 2000);
    },
    resetQuestionState() {
      this.selectedOption = '';
      this.showResult = false;
      this.isCorrect = false;
      this.showCorrectAnswer = false;
    },
    exitQuiz() {
      this.quiz.isPlaying = false;
      this.quiz.Ans = true;
      this.currentQuiz = null;
      this.quiz.currentSlideIndex = 0;
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

/*радио кнопки */
/* From Uiverse.io by srinivasaiml */ 
.quantum-radio {
  position: relative;
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  cursor: pointer;
}
.radio-label {
  color: aqua;
}

.quantum-radio input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
}

.quantum-radio .radio-control {
  position: relative;
  width: 24px;
  height: 24px;
  border: 2px solid #4a4a8a;
  border-radius: 50%;
  margin-right: 15px;
  transition: all 0.3s ease;
  overflow: hidden;
}

.quantum-radio .radio-control::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: conic-gradient(
    from 90deg,
    #00ffcc,
    #00b3ff,
    #0066ff,
    #00b3ff,
    #00ffcc
  );
  border-radius: 50%;
  transform: translate(-50%, -50%) rotate(0deg);
  transition: all 0.4s ease;
  opacity: 0;
}

.quantum-radio:hover .radio-control {
  border-color: #00ffcc;
}

.quantum-radio input:checked ~ .radio-control {
  border-color: #00ffcc;
}

.quantum-radio input:checked ~ .radio-control::before {
  width: 24px;
  height: 24px;
  opacity: 1;
  animation: quantum-spin 2s linear infinite;
}

.quantum-radio input:checked ~ .radio-control::after {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 8px;
  height: 8px;
  background: #00ffcc;
  border-radius: 50%;
  transform: translate(-50%, -50%);
  box-shadow: 0 0 5px #00ffcc;
}

@keyframes quantum-spin {
  0% {
    transform: translate(-50%, -50%) rotate(0deg);
  }
  100% {
    transform: translate(-50%, -50%) rotate(360deg);
  }
}

</style>
