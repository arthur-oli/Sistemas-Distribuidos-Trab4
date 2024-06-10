<template>
    <div>
      <h1>Cadastro Bibliotecacd </h1>
      <div>
        <v-row justify='center' align='center'>
          <v-col cols='6'>
            <v-text-field v-model='newBook.title' label='Título' />
          </v-col>
        </v-row>
        <v-row justify='center' align='center'>
          <v-col cols='6'>
            <v-text-field v-model='newBook.author' label='Autor' />
          </v-col>
        </v-row>
        <v-row justify='center' align='center'>
          <v-col cols='6'>
            <v-text-field v-model='newBook.year_published' label='Ano Publicação' />
          </v-col>
        </v-row>
        <v-row justify='end' align='center'>
          <v-col cols='3'>
            <v-btn @click='addBook()' color='light-blue'> Adicionar livro </v-btn>
          </v-col>
        </v-row>
      </div>
      <v-spacer />
      <v-row />
      <v-row>
        <v-col cols='12'>
            <v-card>
              <v-row justify='center' align='center'>
                <v-col cols='10'>
                  <v-data-table :headers='books.headers' :items='books.items'>
                    <!-- eslint-disable-next-line vue/valid-v-slot -->
                    <template v-slot:item.edit='{ item }'>
                      <v-btn elevation="0" icon color="gray" @click="openDialog(item)">
                        <v-icon dark>
                          mdi-pencil
                        </v-icon>
                      </v-btn>
                    </template>
                    <!-- eslint-disable-next-line vue/valid-v-slot -->
                    <template v-slot:item.delete='{ item }'>
                      <v-btn elevation="0" icon color="red" @click="deleteItem(item)">
                        <v-icon dark>
                          mdi-delete
                        </v-icon>
                      </v-btn>
                    </template>
                  </v-data-table> 
                </v-col>
              </v-row>
            </v-card>
        </v-col>
      </v-row>
      <v-dialog v-model='dialog' width='700'>
        <v-card>
          <div>
            <v-row justify='center' align='center'>
              <v-col cols='6'>
                <v-text-field v-model='editBook.title' label='Título' />
              </v-col>
            </v-row>
            <v-row justify='center' align='center'>
              <v-col cols='6'>
                <v-text-field v-model='editBook.author' label='Autor' />
              </v-col>
            </v-row>
            <v-row justify='center' align='center'>
              <v-col cols='6'>
                <v-text-field v-model='editBook.year_published' label='Ano Publicação' />
              </v-col>
            </v-row>
            <v-row justify='end' align='center'>
              <v-col cols='3'>
                <v-btn @click='saveItemEdit()' color='light-blue'> Salvar Livro </v-btn>
              </v-col>
            </v-row>
          </div>          
        </v-card>
      </v-dialog>
    </div>
  </template>
  
  <script>
  import axios from 'axios';

  export default {
    data() {
      return {
        dialog: false,
        books: {
          items: [],
          headers: [
            {
              title: 'Titulo',
              value: 'title',
            },
            {
              title: 'Autor',
              value: 'author'
            },
            {
              title: 'Ano publicado',
              value: 'year_published',
            },
            {
              title: 'Edit',
              value: 'edit',
            },
            {
              title: 'Delete',
              value: 'delete',
            },
        ],
        },
        newBook: {
          title: '',
          author: '',
          year_published: ''
        },
        editBook: {
          title: '',
          author: '',
          year_published: ''
        },
      }
    },
    methods: {
      load: async function () {
        this.fetchBooks();

      },
      fetchBooks() {
        axios.get('http://localhost:8081/books')
          .then(response => {
            this.books.items = response.data;
            console.log(this.books);
          });
      },
      addBook() {
        axios.post('http://localhost:8081/books', this.newBook)
          .then(response => {
            this.books.items.push(response.data);
          });
      },
      updateBook() {
        const book = this.editBook;
        console.log(book);
        axios.put(`http://localhost:8081/books/${book.id}`, book)
          .then(response => {
            console.log(response);
            this.fetchBooks();
          });
      },
      deleteBook(id) {
        axios.delete(`http://localhost:8081/books/${id}`)
          .then(response => {
            console.log(response);
            this.books.items = this.books.items.filter(b => b.id !== id);
          });
        },
        deleteItem(item) {
          const id = Number.parseInt(item.id, 10);
          this.deleteBook(id);
        },
        openDialog(item) {
          this.editBook = { ...item };
          console.log(this.editBook);
          this.dialog = true;
        },
        saveItemEdit() {
          this.updateBook();
          this.dialog = false;
        },
    },
    created() {
      this.load();
    },
  }

  // EU TENTEI...
  // const evtSource = new EventSource("localhost:8081/stream");
  //       evtSource.onmessage = function(event) {
  //           const data = JSON.parse(event.data);
  //           alert(data.message)
  //       };

  </script>
  