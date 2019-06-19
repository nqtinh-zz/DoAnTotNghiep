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
import CreditCard from '../components/function/Credit_Card.vue'
import ChangePassword from '../components/users/ChangePassword/change_password'
import FSmartPeopleCounting from '../components/common/FSmartPeopleCounting.vue'
import store from '../store/index.js'
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
const router = new Router({
  mode: 'history',
  routes: [{
      path: '/home',
      name: 'dashboar_home',
      component: Dashboard,
      meta: {
        title: 'Dashboard'
      },
       
    },
    {
      path: '/',
      name: 'dashboar_intro',
      component: HomeIntro,
      meta: {
        title: 'Home'
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
       
    },
    {
      path: '/firedetect',
      name: 'firedetect',
      component: FireDetect,
      meta: {
        title: 'firedetect'
      },
       
    },
    {
      path: '/resperson',
      name: 'resperson',
      component: ResPerson,
      meta: {
        title: 'resperson'
      },
       
    },
    {
      path: '/creditcard',
      name: 'creditcard',
      component: CreditCard,
      meta: {
        title: 'creditcard'
      },
       
    },
    {
      path: '/rescamera',
      name: 'rescamera',
      component: ResCamera,
      meta: {
        title: 'rescamera'
      },
       
    },
    {
      path: '/profile',
      name: 'profile',
      component: Profile,
      meta: {
        title: 'profile'
      },
       
    },
    {
      path: '/change_password',
      name: 'change password',
      component: ChangePassword,
      meta: {
        title: 'Change password'
      },
       
    },
    {
      path: '/process',
      name: 'process',
      component: Process,
      meta: {
        title: 'process'
      },
       
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
})
router.beforeEach((to, from, next) => {
  document.title = to.meta.title
  next()
})
export default router
