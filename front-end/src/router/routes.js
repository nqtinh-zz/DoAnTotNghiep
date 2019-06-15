import Vue from 'vue'
import Router from 'vue-router'
import SignIn from '@/components/users/SignIn'
import SignUp from '@/components/users/SignUp'
import Dashboard from '../components/common/Dashboard.vue'
import HomeIntro from '@/components/common/HomeIntro'
import NewProject from '../components/project/NewProject'
import AddFsmarDoor from '../components/function/Add_FsmartDoor'
import FireDetect from '../components/function/Add_FireDetect'
import ResPerson from '../components/resource/ResPerson/ResPerson'
import ResCamera from '../components/resource/ResCamera/Res_Camera'
import Profile from '../components/users/UserProfile/user_profile'
import Process from '../components/resource/Process/Process_Manage'
import Error404 from '../components/error/404.vue'
import Error500 from '../components/error/500.vue'
import Forgot_Password from '@/components/users/Forgot_Password'
import FSmartDoor from '../components/common/FSmartDoor.vue'
import FSmartEscape from '../components/common/FSmartEscape.vue'
import ChangePassword from '../components/users/ChangePassword/change_password'
import FSmartPeopleCounting from '../components/common/FSmartPeopleCounting.vue'
import CreditCard from '../components/function/Credit_Card.vue'
import store from '../store/index.js'
import { Trans } from '@/plugins/Translation'
import { i18n } from '@/plugins/i18n.js'
Vue.use(Router)
const ifNotAuthenticated = (to, from, next) => {
  if (!store.getters.isLoggedIn) {
    next()
    return
  }
  next('/home')
}
const ifAuthenticated = (to, from, next) => {

  if (store.getters.isLoggedIn) {
    next()
    return
  }

  next('/')
}

export default [
    {
      path: '/:lang',
      component: {
        template: '<router-view></router-view>'
      },
      beforeEnter (to,from,next){
          const lang = to.params.lang
          if(!['en','vn','ja'].includes(lang)) return next('en')
          if(i18n.locale !== lang)
          {
              i18n.locale = lang
          }
          return next()
      },
      children: [
        {
      path: '/home',
      name: 'dashboar_home',
      component: Dashboard,
      meta: {
        title: 'Dashboard'
      },
      beforeEnter: ifAuthenticated
    },
    {
      path: '/',
      name: 'dashboar_intro',
      component: HomeIntro,
      meta: {
        title: 'Dashboard'
      },
      beforeEnter: ifNotAuthenticated
    },
    {
      path: '/signin',
      name: 'SignIn',
      component: SignIn,
      meta: {
        title: 'Login'
      },
      beforeEnter: ifNotAuthenticated
    },
    {
      path: '/forgot-password',
      name: 'Forgot_Password',
      component: Forgot_Password,
      meta: {
        title: 'Forgot_Password'
      },
      beforeEnter: ifNotAuthenticated
    },
    {
      path: '/signup',
      name: 'SignUp',
      component: SignUp,
      meta: {
        title: 'Register'
      },
      beforeEnter: ifNotAuthenticated
    },
    {
      path: '/new-project',
      name: 'newproject',
      component: NewProject,
      meta: {
        title: 'NewProject'
      },
      beforeEnter: ifAuthenticated
    },
    {
      path: '/FSmartDoor',
      name: 'FSmartDoor',
      component: FSmartDoor,
      meta: {
        title: 'FSmartDoor'
      },
      beforeEnter: ifNotAuthenticated
    },
    {
      path: '/FSmartEscape',
      name: 'FSmartEscape',
      component: FSmartEscape,
      meta: {
        title: 'FSmartEscape'
      },
      beforeEnter: ifNotAuthenticated
    },
    {
      path: '/FSmartPeopleCounting',
      name: 'FSmartPeopleCounting',
      component: FSmartPeopleCounting,
      meta: {
        title: 'FSmartPeopleCounting'
      },
      beforeEnter: ifNotAuthenticated
    },
    {
      path: '/fsmartdoor',
      name: 'fsmartdoor',
      component: AddFsmarDoor,
      meta: {
        title: 'fsmartdoor'
      },
      beforeEnter: ifAuthenticated
    },
    {
      path: '/firedetect',
      name: 'firedetect',
      component: FireDetect,
      meta: {
        title: 'firedetect'
      },
      beforeEnter: ifAuthenticated
    },
    {
      path: '/resperson',
      name: 'resperson',
      component: ResPerson,
      meta: {
        title: 'resperson'
      },
      beforeEnter: ifAuthenticated
    },
    {
      path: '/creditcard',
      name: 'creditcard',
      component: CreditCard,
      meta: {
        title: 'creditcard'
      },
      beforeEnter: ifAuthenticated
    },
    {
      path: '/rescamera',
      name: 'rescamera',
      component: ResCamera,
      meta: {
        title: 'rescamera'
      },
      beforeEnter: ifAuthenticated
    },
    {
      path: '/profile',
      name: 'profile',
      component: Profile,
      meta: {
        title: 'profile'
      },
      beforeEnter: ifAuthenticated
    },
    {
      path: '/change_password',
      name: 'change password',
      component: ChangePassword,
      meta: {
        title: 'Change password'
      },
      beforeEnter: ifAuthenticated
    },
    {
      path: '/process',
      name: 'process',
      component: Process,
      meta: {
        title: 'process'
      },
      beforeEnter: ifAuthenticated
    },
    {
      path: '/500',
      name: 'error500',
      component: Error500,
    },
    {
      path: '*',
      name: 'error404',
      component: Error404,
    },
      ]
    },
    {
      // Redirect user to supported lang version.
      path: '*',
      redirect (to) {
        return Trans.getUserSupportedLang()
      }
    }
  ]
  