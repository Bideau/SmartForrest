#------------------------------------------------------------
#        Script MySQL.
#------------------------------------------------------------


#------------------------------------------------------------
# Table: sensorType
#------------------------------------------------------------

CREATE TABLE sensorType(
        st_id   int (11) Auto_increment  NOT NULL ,
        st_type Varchar (50) NOT NULL ,
        PRIMARY KEY (st_id )
)ENGINE=InnoDB;

#------------------------------------------------------------
# Table: station
#------------------------------------------------------------

CREATE TABLE station(
        sta_id        int (11) Auto_increment  NOT NULL ,
        sta_name      Varchar (50) NOT NULL ,
        sta_longitude Float NOT NULL ,
        PRIMARY KEY (sta_id )
)ENGINE=InnoDB;

#------------------------------------------------------------
# Table: measure
#------------------------------------------------------------

CREATE TABLE measure(
        m_id    int (11) Auto_increment  NOT NULL ,
        m_date  Date NOT NULL ,
        m_value Float NOT NULL ,
        s_id    Int NOT NULL ,
        PRIMARY KEY (m_id )
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: sensor
#------------------------------------------------------------

CREATE TABLE sensor(
        s_id   int (11) Auto_increment  NOT NULL ,
        st_id  Int NOT NULL ,
        sta_id Int NOT NULL ,
        PRIMARY KEY (s_id )
)ENGINE=InnoDB;

ALTER TABLE measure ADD CONSTRAINT FK_measure_s_id FOREIGN KEY (s_id) REFERENCES sensor(s_id);
ALTER TABLE sensor ADD CONSTRAINT FK_sensor_st_id FOREIGN KEY (st_id) REFERENCES sensorType(st_id);
ALTER TABLE sensor ADD CONSTRAINT FK_sensor_sta_id FOREIGN KEY (sta_id) REFERENCES station(sta_id);
