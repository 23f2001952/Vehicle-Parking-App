import {createWebHistory,createRouter} from 'vue-router'
import HomePage from './pages/HomePage.vue'
import LoginPage from './pages/LoginPage.vue'
import Dashboard from './pages/Dashboard.vue'
import AdminDashboard from './components/AdminDashboard.vue';
import UserDashboard from './components/UserDashboard.vue';
import RegisterPage from './pages/RegisterPage.vue'
import UsersPage from './pages/UsersPage.vue'
import SummaryPage from './pages/SummaryPage.vue'
import UserSummaryPage from './pages/UserSummaryPage.vue'

const routes = [
    {path: "/", component: HomePage},
    {path: "/login", component: LoginPage},
    {
        path : "/dashboard", component : Dashboard,
        meta : {requiresAuth : true},
        children :[   
            { path: "admin", component : AdminDashboard , meta : {role: 'admin'}},
            { path: "user", component : UserDashboard, meta : {role: 'user'}}
        ]
    },
    {path: '/register',component : RegisterPage},
    {path: '/Users', component: UsersPage, meta: {requiresAuth: true, role: 'admin'}},
    {path: '/Summary', component: SummaryPage, meta: {requiresAuth: true}},
    {path: '/UserSummary', component: UserSummaryPage, meta: {requiresAuth: true, role: 'user'}}
]





export const router = createRouter(
    {
        history: createWebHistory(),
        routes
    }
)

