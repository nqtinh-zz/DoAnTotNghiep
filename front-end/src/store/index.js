import Vue from 'vue'
import Vuex from 'vuex'
import auth from './modules/auth'
import project from './modules/project'
import res_group from './modules/res_group'
import res_people from './modules/res_people'
import res_camera from './modules/res_camera/res_camera'
import res_group_camera from './modules/res_camera/res_group_camera'
import abc_process from './modules/process/process'
import user_info from './modules/user/user'
import functionx from './modules/functions'

Vue.use(Vuex)
const debug = process.env.NODE_ENV !== 'production'
export default new Vuex.Store({
  modules: {
    auth,
    project,
    res_group,
    res_people,
    res_camera,
    res_group_camera,
    abc_process,
    user_info,
    functionx,
  },
  strict: debug && false
})
