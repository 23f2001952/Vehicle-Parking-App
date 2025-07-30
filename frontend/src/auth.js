import { reactive } from "vue";

export const auth = reactive(
    {
        loggedIn : localStorage.getItem('loggedIn') === 'true',
        role : localStorage.getItem('role'),

        login(role)
        {
            this.loggedIn = true;
            this.role = role;
            localStorage.setItem('loggedIn',true);
            localStorage.setItem('role',role);
        },

        logout()
        {
            this.loggedIn = false;
            this.role = '';
            localStorage.clear();
        }
    }
)