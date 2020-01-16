import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL")) 
                                                    
db = scoped_session(sessionmaker(bind=engine))

def main():
    b = open("books.csv")
    bookList = csv.DictReader(b) #returns a dict for each row in the csv file. keynames are given by the values in the first row
    for row in bookList:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", {"isbn":row["isbn"], "title":row["title"], "author":row["author"], "year":row["year"]})
        print("inserted book")
    db.commit()

if __name__=="__main__":
    main()
    