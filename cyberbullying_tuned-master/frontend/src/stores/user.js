import { defineStore } from "pinia";

export const useUserStore = defineStore("user", {
  state: () => ({
    name: null,
    age: null,
    ethnicity: null,
  }),
  actions: {
    setUserInfo(name, age, ethnicity) {
      this.name = name;
      this.age = age;
      this.ethnicity = ethnicity;
    },
  },
});
