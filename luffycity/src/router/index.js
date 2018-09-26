import Vue from 'vue'
import Router from 'vue-router'
import HomeBanner from '@/components/LuffyCityHeader/HomeBanner'
import Course from '@/components/LuffyCityHeader/Course'
import LightCourse from '@/components/LuffyCityHeader/LightCourse'
import Micro from '@/components/LuffyCityHeader/Micro'
import QuestionBank from '@/components/LuffyCityHeader/QuestionBank'
import PublicClass from '@/components/LuffyCityHeader/PublicClass'
import InternalMaterials from '@/components/LuffyCityHeader/InternalMaterials'
import AboutUs from '@/components/LuffyCityFooter/AboutUs'
import CallUs from '@/components/LuffyCityFooter/CallUs'
import Business from '@/components/LuffyCityFooter/Business'
import HelpCenter from '@/components/LuffyCityFooter/HelpCenter'
import Feedback from '@/components/LuffyCityFooter/Feedback'
import BeginnerGuide from '@/components/LuffyCityFooter/BeginnerGuide'

import Total from '@/components/LuffyCityHeader/FreeCourse/Total'
import Python from '@/components/LuffyCityHeader/FreeCourse/Python'
import Linux from '@/components/LuffyCityHeader/FreeCourse/Linux'
import FrontEnd from '@/components/LuffyCityHeader/FreeCourse/FrontEnd'
import PythonAdvance from '@/components/LuffyCityHeader/FreeCourse/PythonAdvance'
import UI from '@/components/LuffyCityHeader/FreeCourse/UI'
import Tool from '@/components/LuffyCityHeader/FreeCourse/Tool'

import Login from '../components/Login'

import Detail from '../components/LuffyCityHeader/FreeCourse/Detail'

Vue.use(Router);

export default new Router({
  mode: "history",
  routes: [
    {
      path: "/",
      redirect: '/home',
    },
    {
      path: '/home',
      name: 'home',
      component: HomeBanner
    },
    {
      path: '/course',
      name: 'course',
      component: Course,
      children: [
        {
          path: '/course',
          redirect: '/course/total'
        },
        {
          path: '/course/total',
          name: 'total',
          component: Total,
        },
        {
          path: '/course/python',
          name: 'python',
          component: Python,
        },
        {
          path: '/course/linux',
          name: 'linux',
          component: Linux
        },
        {
          path: '/course/front_end',
          name: 'front_end',
          component: FrontEnd
        },
        {
          path: '/course/python_advance',
          name: 'python_advance',
          component: PythonAdvance
        },
        {
          path: '/course/ui',
          name: 'ui',
          component: UI
        },
        {
          path: '/course/tool',
          name: 'tool',
          component: Tool
        },
      ]
    },
    {
      path: '/light-course',
      name: 'light-course',
      component: LightCourse
    },
    {
      path: '/micro',
      name: 'micro',
      component: Micro
    },
    {
      path: '/questionbank',
      name: 'questionbank',
      component: QuestionBank
    },
    {
      path: '/publicclass',
      name: 'publicclass',
      component: PublicClass
    },
    {
      path: '/internalmaterials',
      name: 'internalmaterials',
      component: InternalMaterials
    },
    {
      path: '/about_us',
      name: 'about_us',
      component: AboutUs
    },
    {
      path: '/call_us',
      name: 'call_us',
      component: CallUs
    },
    {
      path: '/business_cooperation',
      name: 'business_cooperation',
      component: Business
    },
    {
      path: '/help_center',
      name: 'help_center',
      component: HelpCenter
    },
    {
      path: '/feedback',
      name: 'feedback',
      component: Feedback
    },
    {
      path: '/beginner_guide',
      name: 'beginner_guide',
      component: BeginnerGuide
    },
    {
      path:'/login',
      name:'login',
      component:Login,
    }
  ]
})
