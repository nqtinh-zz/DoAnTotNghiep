<template>
  <v-dialog v-model="dialog_credit_card" persistent max-width="1000px">
    <div style="background-color:#F4F3EF">
      <form ref="form" class="card-form" @submit.prevent="add_credit" style="margin-left:2%">
        <header>
          <h1 class="card-form__title">Your card data</h1>
        </header>
        <div class="card-form-field">
          <label for="cardNumberInput" class="card-form-field__label">Number</label>
          <input
            type="text"
            name="card[number]"
            v-model="card.number"
            maxlength="16"
            class="card-form-field__input"
            ref="card.number"
            required
            id="cardNumberInput"
          >
        </div>
        <div class="card-form-field">
          <label for="cardOwnerInput" class="card-form-field__label">Owner name</label>
          <input
            type="text"
            required
            name="card[owner]"
            v-model="card.owner"
            class="card-form-field__input"
            maxlength="24"
            ref="card.owner"
            id="cardOwnerInput"
          >
        </div>
        <div class="card-form-field">
          <label for class="card-form-field__label card-form-field__label_inline">Expiration</label>
          <select
            v-model="card.expiration.month"
            name="card[expiration][month]"
            class="card-form-field__select"
            required
            ref="card.expiration.month"
          >
            <option v-for="month in months">{{month}}</option>
          </select>
          /
          <select
            v-model="card.expiration.year"
            name="card[expiration][year]"
            class="card-form-field__select"
            required
            ref="card.expiration.year"
          >
            <option v-for="year in years">{{year}}</option>
          </select>
        </div>
        <div class="card-form-field">
          <label for="cardCvcInput" class="card-form-field__label card-form-field__label_inline">CVC</label>
          <input
            type="text"
            name="card[cvc]"
            v-model="card.cvc"
            maxlength="3"
            required
            class="card-form-field__input card-form-field__input_cvc"
            id="cardCvcInput"
            ref="card.cvc"
          >
        </div>
        <button type="submit" class="card-form__submit">Checkout</button>
      </form>

      <div class="card-preview" >
        <div class="card-preview__side card-preview__side_back">
          <div class="card-preview__cvc">
            <span class="card-preview__label">CVC</span>
            {{card.cvc}}
          </div>
        </div>
        <div class="card-preview__side card-preview__side_front">
          <div class="card-preview__number">
            <div class="card-preview__label card-preview__label_white">Number</div>
            <div class="card-preview__etched-text">{{cardNumberFormatted}}</div>
          </div>

          <div class="card-preview__owner">
            <span class="card-preview__label card-preview__label_white">Owner</span>
            <span class="card-preview__etched-text">{{card.owner}}</span>
          </div>

          <div class="card-preview__expiration">
            <span class="card-preview__label card-preview__label_white">Valid thru</span>
            <span class="card-preview__etched-text">{{cardExpiration}}</span>
          </div>
        </div>
      </div>
      <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" flat @click="close_dialog" style="font-size: 16px">{{$t(`res_person.cancel`) }}</v-btn>
              
            </v-card-actions>
    </div>
  </v-dialog>
</template>

<script>
export default {
  data() {
    return {
      dialog_credit_card: true,
      card: {
        number: "",
        owner: "",
        expiration: {
          month: "",
          year: ""
        },
        cvc: ""
      }
    };
  },
  methods: {
    formatCardNumber: function() {
      var formattedNumber = "";
    },
    close_dialog: function(){
        this.dialog_credit_card=false;
    },
    add_credit: function(){
        console.log('okkk')
        let data = {
        function_id: 1,
        project_id: JSON.parse(localStorage.getItem("project_id"))
      };
      this.$store.dispatch("add_function_to_project", data).then(async resp => {
        console.log(resp.code);
        let data1 = {
          project_id: JSON.parse(localStorage.getItem("project_id"))
        };
        await this.$store
          .dispatch("get_all_function", data1)
          .then(resp1 => {
            localStorage.setItem(
              "all_function",
              JSON.stringify(resp1.data.data)
            );
            this.functions = JSON.parse(localStorage.getItem("all_function"));
          })
          .catch(err1 => {
            console.log(err1);
          });

        if (resp.code === 0) {
          location.reload();
        }
      });
    },
  },

  computed: {
    cardNumberFormatted: function() {
      var numberChunks = this.card.number.match(/.{1,4}/g);

      if (numberChunks) return numberChunks.join(" ");
      else return "";
    },
    cardExpiration: function() {
      if (!this.card.expiration.month || !this.card.expiration.year) return "";

      return this.card.expiration.month + "/" + this.card.expiration.year;
    },

    months: function() {
      return [
        "01",
        "02",
        "03",
        "04",
        "05",
        "06",
        "07",
        "08",
        "09",
        "10",
        "11",
        "12"
      ];
    },
    years: function() {
      var years = [];
      var currentYear = new Date().getFullYear() % 2000;

      for (var i = 0; i < 18; i++) years.push(currentYear + i);

      return years;
    }
  },

  watch: {
    "card.number": function(newNumber) {
      this.card.number = newNumber.replace(/[^0-9]/gim, "");
    },
    "card.owner": function(newOwner) {
      this.card.owner = newOwner.toUpperCase().replace(/[^A-Z\s]/gim, "");
    },
    "card.cvc": function(newCvc) {
      this.card.cvc = newCvc.replace(/[^0-9]/gim, "");
    }
  },

  mounted: function() {
    var instance = this;

    console.log(this);

    this.$refs.form.addEventListener("submit", function(e) {
      e.stopPropagation();
      e.preventDefault();
    });
  }
};
</script>

<style lang="scss" scoped>
@import url("https://fonts.googleapis.com/css?family=Montserrat");

$bp-sm: 768px;
$bp-md: 1024px;

$black: #000;
$orange: #ff6d00;
$gray: #999;
$white: #fff;

$main-font: "Montserrat", sans-serif;

$transition-speed: 0.3s;

html,
body {
  padding: 0;
  margin: 0;
  cursor: default;
  min-height: 100%;
}

body {
  box-sizing: border-box;
  padding: 16px;
  background-color: $orange;
  font-family: $main-font;
}

#app {
  max-width: 966px;
  margin: 0 auto;
}

.card-form {
  box-sizing: border-box;
  padding: 16px;
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
  background-color: $white;
  box-shadow: 4px 4px 16px rgba($black, 0.8);

  @media (min-width: $bp-sm) {
    margin-top: 64px;
  }
  @media (min-width: $bp-md) {
    display: inline-block;
    margin: 64px 0 0;
  }

  &__title {
    text-align: center;
    color: $orange;
  }
  &__submit {
    padding: 8px 16px;
    border: 1px solid $orange;
    font-size: 18px;
    text-transform: uppercase;
    font-weight: bold;
    border-radius: 2px;
    color: $white;
    background-color: $orange;
    transition: color $transition-speed, background $transition-speed,
      box-shadow $transition-speed;

    &:hover,
    &:focus {
      outline: none;
      color: $orange;
      background-color: $white;
      box-shadow: 0 0 8px $orange;
    }
  }
}

.card-form-field {
  margin: 8px 0 16px;

  &__label {
    display: block;
    margin-bottom: 4px;

    &_inline {
      display: inline-block;
      margin-bottom: 0;
      margin-right: 4px;
    }
  }
  &__input {
    box-sizing: border-box;
    width: 100%;
    padding: 4px 8px;
    font-size: 18px;
    font-family: $main-font;
    border-radius: 2px;
    border: 1px solid $gray;
    transition: box-shadow $transition-speed;

    &:focus {
      outline: none;
      box-shadow: 0 0 8px $orange;
    }

    &_cvc {
      width: 54px;
    }
  }
  &__select {
    box-sizing: border-box;
    padding: 4px 8px;
    font-size: 18px;
    font-family: $main-font;
    background-color: $white;
    border-radius: 2px;
    border: 1px solid $gray;
    transition: box-shadow $transition-speed;

    &:focus {
      outline: none;
      box-shadow: 0 0 8px $orange;
    }
  }
}

.card-preview {
  position: relative;
  display: none;
  vertical-align: top;
  margin-top: calc(64px + 53px);
  margin-left: 32px;
  user-select: none;

  @media (min-width: $bp-md) {
    display: inline-block;
  }

  &__side {
    position: relative;
    width: 400px;
    height: 252px;
    border-radius: 16px;
    background-color: $white;
    box-shadow: 2px 2px 2px rgba($black, 0.5);

    &_front {
      background-color: #009e8e;
      box-shadow: 2px 2px 6px rgba($black, 0.6);
    }
    &_back {
      position: absolute;
      background-color: $white;
      top: 32px;
      left: 128px;
      background-image: linear-gradient(
        to bottom,
        $white 24%,
        $black 24%,
        $black 40%,
        $white 40%
      );
    }
  }
  &__label {
    font-size: 12px;
    color: $gray;
    text-transform: uppercase;

    &_white {
      color: $white;
    }
  }
  &__cvc {
    position: absolute;
    top: 50%;
    left: 280px;
  }
  &__number {
    position: absolute;
    top: 32%;
    left: 16px;
    font-size: 34px;
  }
  &__owner {
    position: absolute;
    left: 16px;
    bottom: 40px;
  }
  &__expiration {
    position: absolute;
    left: 16px;
    bottom: 16px;
  }
  &__etched-text {
    text-shadow: 1px 1px 4px #000;
    color: #fff;
  }
}
</style>

